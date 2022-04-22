#include <Windows.h>
#include <iostream>
#include <vector>
#include <string>
#include <mutex>
#include <chrono>
#include <random>

struct Doctor
{
    int numberOfHealedPatients;      
    int currentPatientID;

    Doctor()
    {
        currentPatientID = -1;
        this->numberOfHealedPatients = 0;
    }
};

struct Patient
{
    int timeToHeal;
    int patientID;

    Patient(int timeToHeal, int patientID)
    {
        this->timeToHeal = timeToHeal;
        this->patientID = patientID;
    }
};

struct Intern
{
    int timeRequired;
    int id;

    Intern(int time, int doctorID)
    {
        this->timeRequired = time;
        this->id = doctorID;
    }
};

const int DAILY_PATIENTS_QUOTA = 5;
HANDLE pipes[5];
std::mutex mtx;
std::vector<Doctor> staff;
std::vector<Patient> patients;
std::vector<Intern> internInLine;
int chiefDoctorSlept = 0;
bool chiefIsAsleep = false;
int patientsHealed = 0;

void printStats() {
    
    for (int i = 0; i < staff.size(); ++i)
    {
        std::cout << (!i ? "chief physician " : ("intern " + std::to_string(i))) << " healed " << staff[i].numberOfHealedPatients << " patients\n";
    }
    
    std::cout << "chief physician slept for " << chiefDoctorSlept;
}

void chiefSleeps()
{
    std::this_thread::sleep_for(std::chrono::seconds(5));
    chiefDoctorSlept += 5;
}

void waitForPatient(int doctorID)
{
    int timeToHeal;
    bool internNeedsHelp;
    while (true)
    {
        std::random_device rd; // seed the random number generator object called mt
        std::mt19937 mt(rd()); // requests for random data to the operating system
        std::uniform_int_distribution<int> dist(0, 10);
        std::this_thread::sleep_for(std::chrono::seconds(1));     
        mtx.lock();  
        if (!doctorID && internInLine.size())
        {
            //mtx.lock();
            // doctor helps one intern to heal a patient                      
            timeToHeal = internInLine[0].timeRequired;
            int internID = internInLine[0].id;
            internInLine.erase(internInLine.begin());
            mtx.unlock();
            // heal the patient
            std::this_thread::sleep_for(std::chrono::seconds(timeToHeal));
            
            mtx.lock();
            staff[internID].numberOfHealedPatients++;     
            std::cout << "patient " << staff[internID].currentPatientID + 1 << " was healed and left the hospital.\n";
            patientsHealed++;
            staff[internID].currentPatientID = -1;
            //mtx.unlock();
            chiefSleeps();
        }
        else if (patients.size())
        {
            //mtx.lock();
            // cheif physician has id = 0
            std::cout << "doctor " << doctorID << " assigned himself patient " << patients[0].patientID + 1 << "\n";
            if (doctorID)
            {
                (dist(mt)%2) ? internNeedsHelp = true : internNeedsHelp = false;
            }

            // remember patient attributes so we can delete it from the vector
            staff[doctorID].currentPatientID = patients[0].patientID;
            timeToHeal = patients[0].timeToHeal;

            patients.erase(patients.begin());
            //mtx.unlock();
            if (doctorID && internNeedsHelp)
            {
                //mtx.lock();
                internInLine.push_back(Intern(timeToHeal, doctorID));
                mtx.unlock();

                // wait for cheef physician to mark patient as healed
                while (staff[doctorID].currentPatientID != -1)
                {
                    std::this_thread::sleep_for(std::chrono::seconds(1));
                }
                mtx.lock();
            }
            else
            {
                // doctor heals the patient
                std::this_thread::sleep_for(std::chrono::seconds(timeToHeal));
                staff[doctorID].numberOfHealedPatients++;
            
                // print notification
                std::cout << "patient " << staff[doctorID].currentPatientID + 1 << " was healed and left the hospital.\n";
                patientsHealed++;
                staff[doctorID].currentPatientID = -1;            
            }
        } 

        if (patientsHealed == DAILY_PATIENTS_QUOTA)
        {
            mtx.unlock();
            return;
        }
        else
        {
            mtx.unlock();
        }
    }
}

void putPatientInLine(int index)
{
    mtx.lock();    
    DWORD dwBytes;
    int timeToHeal;
    if (!ReadFile(pipes[index], &timeToHeal, sizeof(timeToHeal), &dwBytes, NULL))
    {
        std::cout << "reading error on index " << index << std::endl;
        timeToHeal = 10; // set default value
    }
    std::cout << "patient " << index + 1 << " has arrived. time required: " << timeToHeal << std::endl;
    patients.push_back(Patient(timeToHeal, index));
    mtx.unlock();
}

int main()
{
    int num = 0;

    // spawn doctor threads and fill the staff vector
    // TODO maybe add new thread property for Doctor struct -> change .join()

    std::thread* doctors = new std::thread[5];
    for (int i = 0; i < 5; ++i)
    {
        staff.push_back(Doctor());
        doctors[i] = std::thread(waitForPatient, i);
    }

    while (num < DAILY_PATIENTS_QUOTA)
    {       
        HANDLE pipe = CreateNamedPipe(TEXT("\\\\.\\pipe\\mypipe1"), 
                PIPE_ACCESS_DUPLEX, PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
                PIPE_UNLIMITED_INSTANCES, 1, 1, 0, NULL);
        while (true)
        {
            if (ConnectNamedPipe(pipe, 0)) break;
        }

        pipes[num] = pipe;
        putPatientInLine(num++);
        CloseHandle(pipe);

        if (num == DAILY_PATIENTS_QUOTA)
        {
            // wait for all patients to leave
            while (patientsHealed != DAILY_PATIENTS_QUOTA) Sleep(1000);
        }
    }  

    for (int i = 0; i < 5; ++i) doctors[i].join();    
    delete[] doctors;
    printStats();
    return 0;
}

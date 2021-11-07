package root;

import java.io.FileInputStream;
import java.io.IOException;

public class ArbitraryFileLoader extends ClassLoader {

    public Class loadClassFromFile(final String filename) throws IOException {
        final byte[] b = this.loadClassData(filename);
        return this.defineClass(null, b, 0, b.length);
    }

    private byte[] loadClassData(final String filename) throws IOException {
        byte[] fileContent;
        try (final FileInputStream in = new FileInputStream(filename)) {
            fileContent = new byte[in.available()];
            in.read(fileContent);
        }
        return fileContent;
    }

}

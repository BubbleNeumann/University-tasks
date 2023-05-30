#![allow(dead_code)]

use std::fmt::Display;
use std::{ops, println};

// #[path = "common.rs"]
mod common;

use crate::common::*;

#[path = "lab2.rs"]
mod lab2;

use crate::lab2::{magnitude, zip_map, Func, VecMutRef, VecRef};

#[path = "lab3.rs"]
mod lab3;

use crate::lab3::{gradient, partial_derivative};

#[derive(Debug)]
pub struct Matrix {
    elems: Vec<Vec<f64>>,
    rows: usize,
    cols: usize,
}

impl Matrix {
    /// constructor
    fn zeros(rows: usize, cols: usize) -> Matrix {
        Matrix {
            elems: vec![vec![0.; cols]; rows],
            rows,
            cols,
        }
    }

    /// constructor
    fn identity(size: usize) -> Matrix {
        let mut identity = Matrix {
            elems: vec![vec![]; size],
            rows: size,
            cols: size,
        };
        for ind in 0..size.pow(2) {
            identity.elems[ind / size].push(if ind / size == ind % size { 1. } else { 0. });
        }
        identity
    }

    /// returns lower and upper triangular matrices
    fn lu(&self) -> (Matrix, Matrix) {
        if self.rows != self.cols {
            panic!("lu decomposition : non square matrix");
        }
        let mut up = Matrix::identity(self.rows);
        let mut low = Matrix::identity(self.rows);

        for i in 0..self.rows {
            for j in 0..self.cols {
                if j >= i {
                    low.elems[j][i] = self.elems[j][i]
                        - (0..i)
                            .map(|k| low.elems[j][k] * up.elems[k][i])
                            .sum::<f64>();
                }
            }
            for j in 0..self.cols {
                if j > i {
                    up.elems[i][j] = self.elems[i][j] / low.elems[i][i]
                        - (0..i)
                            .map(|k| (low.elems[i][k] * up.elems[k][j]) / low.elems[i][i])
                            .sum::<f64>();
                }
            }
        }
        (low, up)
    }

    fn linsolve(&self, b: VecRef) -> Vec<f64> {
        let (low, up) = self.lu();
        let (mut res, mut z) = (vec![0.; self.rows], vec![0.; self.rows]);
        for i in 0..self.rows {
            z[i] = (b[i] - (0..i).map(|j| z[j] * low.elems[i][j]).sum::<f64>()) / low.elems[i][i];
        }
        for i in (0..self.rows).rev() {
            res[i] = z[i]
                - (i + 1..self.rows)
                    .map(|j| res[j] * up.elems[i][j])
                    .sum::<f64>();
        }
        res
    }

    fn invert(&self) -> Matrix {
        let mut inv = Matrix::zeros(self.rows, self.cols);
        let mut b = vec![0.; self.rows];
        let mut col: Vec<f64>;
        for i in 0..self.cols {
            b[i] = 1.;
            col = self.linsolve(&b);
            b[i] = 0.;
            for j in 0..self.rows {
                inv.elems[j][i] = col[j];
            }
        }
        inv
    }
}

/// overload multiplication for Matrix and Vec
impl ops::Mul<Vec<f64>> for Matrix {
    type Output = Vec<f64>;

    fn mul(self, rhs: Vec<f64>) -> Self::Output {
        self.elems
            .iter()
            .map(|x| zip_map(&x, &rhs, &|a, b| a * b).iter().sum())
            .collect()
    }
}

/// define Matrix multiplication behavior
impl ops::Mul<Matrix> for Matrix {
    type Output = Matrix;

    fn mul(self, rhs: Matrix) -> Self::Output {
        let mut res = Matrix::zeros(self.cols, rhs.rows);
        for row in 0..res.rows {
            for col in 0..res.cols {
                for k in 0..rhs.rows {
                    res.elems[row][col] += self.elems[row][k] * rhs.elems[k][col];
                }
            }
        }
        res
    }
}

impl Display for Matrix {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for row in self.elems.iter() {
            writeln!(f, "{:?}", row).unwrap();
        }
        Ok(())
    }
}

/// second partial derivative
fn part2(func: Func, x: VecMutRef, ind0: &usize, ind1: &usize) -> f64 {
    x[*ind1] -= EPS;
    let f_l = partial_derivative(func, x, ind0);
    x[*ind1] += 2. * EPS;
    let f_r = partial_derivative(func, x, ind0);
    x[*ind1] -= EPS;
    (f_r - f_l) / EPS * 0.5
}

fn hessian(func: Func, x0: VecMutRef) -> Matrix {
    let size = x0.len();
    let mut hes = Matrix::zeros(size, size);
    let (mut row, mut col): (usize, usize);
    for ind in 0..size.pow(2) {
        (row, col) = (ind / size, ind % size);
        hes.elems[row][col] = part2(func, x0, &row, &col);
    }

    hes
}

fn newton_raphson(func: Func, start: VecRef) -> Vec<f64> {
    let mut x_i = start.clone();
    let mut x_i_1: Vec<f64>;
    let mut grad: Vec<f64>;
    let mut hess: Matrix;
    for _ in 0..ITERS_MAX {
        grad = gradient(func, &x_i);
        hess = hessian(func, &mut x_i.clone()).invert();
        x_i_1 = zip_map(&x_i, &(hess * grad), &|a, b| a - b);
        if magnitude(&zip_map(&x_i_1, &x_i, &|x, y| x - y)) < EPS {
            break;
        }
        x_i = x_i_1;
    }
    x_i
}

fn heaviside(vec: VecRef) -> Vec<f64> {
    let mut res = vec![0.; vec.len()];
    for i in 0..vec.len() {
        res[i] = if vec[i] >= 0. { 1. } else { 0. };
    }
    res
}

// supposedly works
fn bounded_func(args: VecRef) -> f64 {
    fn external_penalty(x: VecRef, N: Matrix, d: VecRef) -> f64 {
        let dist = zip_map(&(N * x.clone()), d, &|a, b| a - b);
        heaviside(&dist.iter().map(|x| x.powf(-4.)).collect())
            .iter()
            .sum()
    }
    let N = Matrix {
        elems: vec![vec![7., -2.], vec![1., 1.], vec![-7., 7.]],
        rows: 3,
        cols: 2,
    };
    let d = vec![0., 0., 0.];
    (args[0] - 4.).powf(2.) + (args[1] - 4.).powf(2.) + external_penalty(args, N, &d)
}

// !! this doesn't work
fn bounded_func_with_internal_penalty(args: VecRef) -> f64 {
    fn internal_penalty(x: VecRef, N: Matrix, d: VecRef) -> f64 {
        zip_map(&(N * x.clone()), d, &|a, b| a - b)
            .iter()
            .sum::<f64>()
            .powf(-4.)
    }

    let N = Matrix {
        elems: vec![vec![7., -2.], vec![1., 1.], vec![-7., 7.]],
        rows: 3,
        cols: 2,
    };
    let d = vec![0., 0., 0.];
    (args[0] - 4.).powf(2.) + (args[1] - 4.).powf(2.) + internal_penalty(args, N, &d)
}

// lab 5
// simplex method
struct Simplex {
    bounds_matrix: Matrix,
    bounds_vec: Vec<f64>,
    inequalities: Vec<i32>,
    simplex_table: Matrix,
    basis_args: Vec<usize>, // list of basis arguments indices
    func_mod_args: Vec<usize>,
    natural_args_ind: Vec<usize>,
    prices_vec: Vec<f64>,
}

impl Simplex {
    fn is_target_modified(&self) -> bool {
        self.func_mod_args.len() > 0
    }

    fn is_plan_optimal(&self) -> bool {
        let row = self.simplex_table.elems[self.simplex_table.rows - 1].clone();

        // check that all row elements are positive
        let mut opt = row.iter().filter(|x| **x > 0.).collect::<Vec<_>>().len() == row.len();
        if self.is_target_modified() {
            if !opt {
                return opt;
            }

            let row = self.simplex_table.elems[self.simplex_table.rows - 2].clone();
            opt = row.iter().filter(|x| **x > 0.).collect::<Vec<_>>().len() == row.len();
        }
        opt
    }

    fn get_main_col(&self) -> i32 {
        let row = self.simplex_table.elems[self.simplex_table.rows - 1].clone();
        let mut ind: i32 = -1;
        let mut delta = 0.;
        for (i, elem) in row.into_iter().enumerate() {
            if elem < delta {
                delta = elem;
                ind = i as i32;
            }
        }

        if !self.is_target_modified() && ind == -1 {
            return ind;
        }

        let row = self.simplex_table.elems[self.simplex_table.rows - 2].clone();
        for i in self.natural_args_ind.iter() {
            if row[*i] < delta {
                delta = row[*i];
                ind = *i as i32;
            }
        }

        ind
    }

    fn get_main_row(&self, main_col: i32) -> i32 {
        let mut delta = 1e12;
        let mut ind = -1;
        if main_col == -1 {
            return ind;
        }
        let mut aik: f64;
        let b_ind = self.simplex_table.cols - 1;
        let rows_n = if self.is_target_modified() {
            self.simplex_table.rows - 2
        } else {
            self.simplex_table.rows - 1
        };
        for i in 0..rows_n {
            aik = self.simplex_table.elems[i][main_col as usize];
            if aik >= 0. && self.simplex_table.elems[i][b_ind] / aik <= delta {
                delta = self.simplex_table.elems[i][b_ind] / aik;
                ind = i as i32;
            }
        }

        ind
    }

    fn build_virt_basis_col(&mut self, ineq_id: usize, sign: i32) -> (i32, i32) {
        if sign == 1 {
            for row in 0..self.simplex_table.rows {
                if row == ineq_id {
                    self.simplex_table.elems[row].push(-1.);
                    self.simplex_table.elems[row].push(1.);
                } else {
                    self.simplex_table.elems[row].push(0.);
                    self.simplex_table.elems[row].push(0.);
                }
            }
            self.simplex_table.cols += 2;
            return (
                (self.simplex_table.cols - 2) as i32,
                (self.simplex_table.cols - 1) as i32,
            );
        }
        for row in 0..self.simplex_table.rows {
            if row == ineq_id {
                self.simplex_table.elems[row].push(1.);
            } else {
                self.simplex_table.elems[row].push(0.);
            }
        }
        self.simplex_table.cols += 1;
        ((self.simplex_table.cols - 1) as i32, -1)
    }

    fn build_simplex_table(&mut self) {
        self.simplex_table = Matrix {
            elems: self.bounds_matrix.elems.clone(),
            rows: self.bounds_matrix.rows,
            cols: self.bounds_matrix.cols,
        };

        for row in 0..self.simplex_table.rows {
            if self.bounds_vec[row] < 0. {
                self.inequalities[row] *= -1;
                self.bounds_vec[row] *= -1.;
                self.simplex_table.elems[row] = self.simplex_table.elems[row]
                    .iter()
                    .map(|x| x * -1.)
                    .collect();
            }

            self.natural_args_ind = (0..self.prices_vec.len()).collect();

            let mut basis_args: (i32, i32);
            for ineq_ind in 0..self.inequalities.len() {
                basis_args = self.build_virt_basis_col(ineq_ind, self.inequalities[ineq_ind]);
                self.natural_args_ind.push(basis_args.0 as usize);
                if basis_args.1 != -1 {
                    self.basis_args.push(basis_args.1 as usize);
                    self.func_mod_args.push(basis_args.1 as usize);
                } else {
                    self.basis_args.push(basis_args.0 as usize);
                }
            }

            let mut sim_diff: Vec<f64> = vec![];
            for j in 0..self.simplex_table.cols {
                // simplex problem type == max
                sim_diff.push(if j < self.prices_vec.len() {
                    -self.prices_vec[j]
                } else {
                    0.
                });
                // simplex problem type == min
                // sim_diff.push(if j < self.prices_vec.len() {
                //     self.prices_vec[j]
                // } else {
                //     0.
                // });
            }

            self.simplex_table.elems.push(sim_diff);
            self.simplex_table.rows += 1;
            if !self.is_target_modified() {
                return;
            }

            let mut sim_diff_add = vec![0.; self.simplex_table.cols];
            for func_mod_arg in self.func_mod_args.iter() {
                sim_diff_add[*func_mod_arg] = 1.;
            }
            self.simplex_table.elems.push(sim_diff_add);
            self.simplex_table.rows += 1;
        }
    }

    fn cur_simplex_solution(&self, only_natural_args: bool) -> Vec<f64> {
        let mut solution = vec![
            0.;
            if only_natural_args {
                self.prices_vec.len()
            } else {
                self.simplex_table.cols - 1
            }
        ];
        for i in 0..self.basis_args.len() {
            if self.basis_args[i] < solution.len() {
                solution[self.basis_args[i]] =
                    self.simplex_table.elems[i][self.simplex_table.cols - 1];
            }
        }
        solution
    }

    fn validate(&self) -> bool {
        let mut val = 0.;
        let n_rows = if self.is_target_modified() {
            self.simplex_table.rows - 2
        } else {
            self.simplex_table.rows - 1
        };
        let n_cols = self.simplex_table.cols - 1;
        for i in 0..self.basis_args.len() {
            if self.basis_args[i] < self.prices_vec.len() {
                val += self.simplex_table.elems[i][n_cols] * self.prices_vec[self.basis_args[i]];
            }
        }
        // mode == max
        if (val - self.simplex_table.elems[n_rows][n_cols]).abs() < 1e-5 {
            return if self.is_target_modified() {
                (self.simplex_table.elems[self.simplex_table.rows - 1][self.simplex_table.cols - 1])
                    .abs()
                    < 1e-5
            } else {
                true
            };
        }
        // mode == min
        // if (val + self.simplex_table.elems[n_rows][n_cols]).abs() < 1e-5 {
        //     return if self.is_target_modified() {
        //         (self.simplex_table.elems[self.simplex_table.rows - 1]
        //             [self.simplex_table.cols - 1])
        //             .abs() < 1e-5
        //     } else {
        //         true
        //     };
        // }
        false
    }

    fn solve(&mut self) {
        let mut solution: Vec<f64>;
        self.build_simplex_table();
        println!("\n initial simplex_table\n{}", self.simplex_table);
        while !self.is_plan_optimal() {
            let main_col = self.get_main_col();
            let main_row = self.get_main_row(main_col);

            println!("{} {}", main_row, main_col);
            // TODO here should be writing to simplex table history
            // but do we need it?

            if main_col == -1 || main_row == -1 {
                break;
            }


            let main_elem = self.simplex_table.elems[main_row as usize][main_col as usize];
            self.basis_args[main_row as usize] = main_col as usize;

            // divide all elements of main row by main element of simplex table
            self.simplex_table.elems[main_row as usize] = self.simplex_table.elems
                [main_row as usize]
                .iter()
                .map(|x| x / main_elem)
                .collect();

            for row_id in 0..self.simplex_table.rows {
                if row_id != main_row as usize {

                    // TODO thoroughly test this. my goodness
                    self.simplex_table.elems[row_id] = self.simplex_table.elems[row_id]
                        .iter()
                        .zip(
                            self.simplex_table.elems[main_row as usize]
                                .iter()
                                .map(|x| x * self.simplex_table.elems[row_id][main_col as usize]),
                        )
                        .map(|(x, y)| x - y)
                        .collect();
                }
            }
            println!("{}", self.simplex_table);
            println!("{:?}", self.basis_args);
            solution = self.cur_simplex_solution(false);
            println!("{:?}", solution);
        }

        println!("\nfinal simplex_table\n{}", self.simplex_table);
        solution = self.cur_simplex_solution(true);
        println!("{:?}", solution);
        // if self.validate() {
        //     solution = self.cur_simplex_solution(true);
        //     println!("{:?}", solution);
        // }
    }
}

fn main() {
    let mut sm = Simplex {
        bounds_matrix: Matrix {
            elems: vec![vec![-2., 6.], vec![3., 2.], vec![2., -1.]],
            rows: 3,
            cols: 2,
        },
        bounds_vec: vec![40., 28., 14.],
        inequalities: vec![-1, -1, -1],
        natural_args_ind: vec![],
        basis_args: vec![],
        func_mod_args: vec![],
        simplex_table: Matrix {
            elems: vec![],
            rows: 0,
            cols: 0,
        },
        prices_vec: vec![2., 3.],
    };
    sm.solve();
}

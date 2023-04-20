#![allow(dead_code)]

use std::fmt::Display;
use std::ops;

mod common;

use crate::common::*;

#[path = "lab2.rs"]
mod lab2;

use crate::lab2::{magnitude, zip_map, Func, VecMutRef, VecRef};

#[path = "lab3.rs"]
mod lab3;

use crate::lab3::{gradient, partial_derivative};

#[derive(Debug)]
struct Matrix {
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
                    low.elems[j][i] = self.elems[j][i].clone();
                    for k in 0..i {
                        low.elems[j][i] -= low.elems[j][k] * up.elems[k][i];
                    }
                }
            }
            for j in 0..self.cols {
                if j > i {
                    up.elems[i][j] = self.elems[i][j] / low.elems[i][i];
                    for k in 0..i {
                        up.elems[i][j] -= (low.elems[i][k] * up.elems[k][j]) / low.elems[i][i];
                    }
                }
            }
        }

        (low, up)
    }

    fn rank(&self) -> i32 {
        let mut rank = 0;
        for i in 0..self.rows {
            let mut j: usize = 0;
            let row_selected = vec![false; self.rows];
            loop {
                if !row_selected[j] && self.elems[j][i].abs() > EPS {
                    break;
                }
                j += 1;
            }
            // if j != self.rows {
            //     rank += 1;
            //     row_selected[j] = true;
            //     for
            //
            // }
        }

        rank
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
        let (mut b, mut col) = (vec![0.; self.rows], vec![0.; self.rows]);
        for i in 0..self.cols {
            b[i] = 1.;
            col = self.linsolve(&b);
            b[i] = 0.;
            // let _ = (0..self.rows).map(|j| inv.elems[j][i] = col[j]);
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

fn main() {
    let mut m = Matrix {
        elems: vec![vec![8., 1., 6.], vec![3., 5., 7.], vec![4., 9., 2.]],
        rows: 3,
        cols: 3,
    };
    println!("{}", m.lu().0);
    println!("{}", m.lu().1);
    println!("{}", m.lu().0 * m.lu().1);
    let inv = m.invert();
    println!("{}", m * inv);
    println!("{:?}", newton_raphson(vec_func, &mut vec![0., 0.]));
}

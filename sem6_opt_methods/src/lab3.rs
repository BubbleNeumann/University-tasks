#[allow(dead_code)]
mod common;
use crate::common::*;

#[path = "lab2.rs"]
mod lab2;
use crate::lab2::*;

fn partial_derivative(func: Func, x: VecMutRef, coord_ind: usize) -> f64 {
    x[coord_ind] += EPS;
    let plus = func(x);
    x[coord_ind] -= 2.0 * EPS;
    let minus = func(x);
    x[coord_ind] += EPS;
    (plus - minus) / EPS * 0.5
}

fn gradient(func: Func, x: VecRef) -> Vec<f64> {
    let mut x_copy = x.clone();
    let mut df: Vec<f64> = vec![0.; x.len()];
    for i in 0..x.len() {
        df[i] = partial_derivative(func, &mut x_copy, i);
    }
    df
}

fn grad_desc(func: Func, start: VecRef) -> Vec<f64> {
    let mut x_i = start.clone();
    let (mut x_i_1, mut grad): (Vec<f64>, Vec<f64>);
    for _ in 0..ITERS_MAX {
        grad = gradient(func, &x_i);
        x_i_1 = zip_map(&x_i, &grad, &|x, y| x - y);
        x_i_1 = bisect(func, &mut x_i, &mut x_i_1);
        if magnitude(&zip_map(&x_i_1, &x_i, &|x, y| x - y)) < EPS {
            break;
        }
        x_i_1.clone_into(&mut x_i);
    }
    x_i
}

fn conj_grad_desc(func: Func, start: VecRef) -> Vec<f64> {
    let mut x_i = start.clone();
    let mut s_i = gradient(func, start);
    let (mut x_i_1, mut s_i_1): (Vec<f64>, Vec<f64>);
    let mut omega: f64;
    for _ in 0..ITERS_MAX {
        x_i_1 = zip_map(&x_i, &s_i, &|x, y| x + y);
        if magnitude(&zip_map(&x_i_1, &x_i, &|x, y| x - y)) < EPS {
            break;
        }
        x_i_1 = bisect(func, &mut x_i, &mut x_i_1);
        s_i_1 = gradient(func, &x_i_1);
        omega = magnitude(&s_i_1).powi(2) / magnitude(&s_i).powi(2);
        s_i = zip_map(&s_i, &s_i_1, &|x, y| x * omega - y);
        x_i = x_i_1.clone();
    }
    x_i
}

fn main() {
    let a = vec![0., 0.];
    println!("{:?}", grad_desc(vec_func, &a));
    println!("{:?}", conj_grad_desc(vec_func, &a));
}

#![allow(dead_code)]
mod common;
use crate::common::*;
use std::vec;

pub type VecRef<'a> = &'a Vec<f64>;
pub type VecMutRef<'a> = &'a mut Vec<f64>;
pub type Func = fn(&Vec<f64>) -> f64;

pub fn zip_map(a: VecRef, b: VecRef, f: &dyn Fn(f64, f64) -> f64) -> Vec<f64> {
    a.iter().zip(b.iter()).map(|(ai, bi)| f(*ai, *bi)).collect()
}

pub fn magnitude(vec: VecRef) -> f64 {
    vec.iter().map(|x| x * x).sum::<f64>().sqrt()
}

pub fn normalize(vec: VecRef) -> Vec<f64> {
    let mag = 1. / magnitude(vec);
    vec.iter().map(|x| x * mag).collect()
}

pub fn bisect(func: Func, a: VecMutRef, b: VecMutRef) -> Vec<f64> {
    let dir = normalize(&zip_map(&a, &b, &|x, y| y - x)); // direction
    let mut xc: Vec<f64> = Vec::with_capacity(a.len());
    for _ in 0..ITERS_MAX {
        if magnitude(&zip_map(&a, &b, &|x, y| (y - x).abs())) < EPS {
            break;
        }

        xc = zip_map(&a, &b, &|x, y| x + y)
            .iter()
            .map(|x| x * 0.5)
            .collect();

        let dir_pos = func(&zip_map(&xc, &dir, &|x, y| x + y));
        let dir_neg = func(&zip_map(&xc, &dir, &|x, y| x - y));

        if dir_pos > dir_neg {
            xc.clone_into(b);
        } else {
            xc.clone_into(a);
        }
    }

    xc
}

fn coord_desc(func: Func, start: VecRef) -> Vec<f64> {
    let mut x0 = start.clone();
    let mut x1 = start.clone();

    let step = 1.;
    let (mut xi, mut y0, mut y1): (f64, f64, f64);

    let mut opt_coord_n = 0;
    let mut coord_id: usize;

    for i in 0..ITERS_MAX {
        coord_id = i % x0.len();
        x1[coord_id] -= EPS;
        y0 = func(&x1);
        x1[coord_id] += 2. * EPS;
        y1 = func(&x1);
        x1[coord_id] -= EPS;
        x1[coord_id] += if y0 > y1 { step } else { -step };
        xi = x0[coord_id];
        x1 = bisect(func, &mut x0, &mut x1);
        x0 = x1.clone();

        if (x1[coord_id] - xi).abs() < EPS {
            opt_coord_n += 1;
            if opt_coord_n == x1.len() {
                return x0;
            }

            continue;
        }

        opt_coord_n = 0;
    }

    x0
}

fn main() {
    let a = vec![0., 0.];
    let res = coord_desc(vec_func, &a);
    println!("{:?}", res);
}

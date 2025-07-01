#include <iostream>
#include <cmath>
#include <vector>
#include <cstdlib>
#include <random>
#include <algorithm>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

float fade(float t)
{
    return t * t * t * (t * (t * 6 - 15) + 10);
}

float lerp(float a, float b, float t)
{
    return a + t * (b - a);
}

float grad(int hash_val, float x, float y)
{
    int h = hash_val & 15;
    float u = (h < 8) ? x : y;
    float v = (h < 4) ? y : (h == 12 || h == 14) ? x
                                                 : 0;

    return (u + v) * ((h & 1) == 0 ? 1 : -1);
}

float perlin(float x, float y, const std::vector<int> &p)
{
    int X = static_cast<int>(std::floor(x)) & 255;
    int Y = static_cast<int>(std::floor(y)) & 255;

    float xf = x - std::floor(x);
    float yf = y - std::floor(y);

    float u = fade(xf);
    float v = fade(yf);

    int aa = p[p[X] + Y];
    int ab = p[p[X] + Y + 1];
    int ba = p[p[X + 1] + Y];
    int bb = p[p[X + 1] + Y + 1];

    return lerp(
        lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u),
        lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u),
        v);
}

std::vector<int> generate_permutation()
{
    std::vector<int> p(256);
    for (int i = 0; i < 256; ++i)
    {
        p[i] = i;
    }

    std::random_device rd;
    std::mt19937 g(rd());

    std::shuffle(p.begin(), p.end(), g);
    p.insert(p.end(), p.begin(), p.end());
    return p;
}

float get_height(float x, float y, const std::vector<int> &permutation, float scale = 0.34)
{
    return perlin(x * scale, y * scale, permutation);
}

PYBIND11_MODULE(noise, m)
{
    m.def("generate_permutation", &generate_permutation, "Generate a permutation table");
    m.def("get_height", &get_height, "Get the height from Perlin noise", py::arg("x"), py::arg("y"), py::arg("permutation"), py::arg("scale") = 0.34);
}

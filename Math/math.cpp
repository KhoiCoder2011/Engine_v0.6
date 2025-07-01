#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <cmath>
#include <algorithm>
#include <random>
#include <sstream>
#include "math.h"
#include <cassert>

namespace py = pybind11;
#define PI 3.14159265358979323846f

float clamp(float value, float min_value, float max_value)
{
    if (value < min_value)
        return min_value;
    if (value > max_value)
        return max_value;
    return value;
}

Vector2::Vector2(float x, float y) : x(x), y(y) {}

glm::vec2 Vector2::to_glm_vec2() const
{
    return glm::vec2(x, y);
}

Vector2 Vector2::operator+(const Vector2 &other) const
{
    return Vector2(x + other.x, y + other.y);
}

Vector2 Vector2::operator-(const Vector2 &other) const
{
    return Vector2(x - other.x, y - other.y);
}

Vector2 Vector2::operator*(float scalar) const
{
    return Vector2(x * scalar, y * scalar);
}

float Vector2::length() const
{
    return glm::length(to_glm_vec2());
}

Vector2 Vector2::normalize() const
{
    float len = length();
    return len != 0 ? *this * (1.0f / len) : Vector2(0, 0);
}

std::string Vector2::to_str() const
{
    std::stringstream ss;
    ss << "(" << x << ", " << y << ")";
    return ss.str();
}

Vector2 Vector2::clamp_vec(const Vector2 &p_min, const Vector2 &p_max) const
{
    return Vector2(
        clamp(x, p_min.x, p_max.x),
        clamp(y, p_min.y, p_max.y));
}

Vector3::Vector3(float x, float y, float z) : x(x), y(y), z(z) {}

glm::vec3 Vector3::to_glm_vec3() const
{
    return glm::vec3(x, y, z);
}

Vector3 Vector3::operator+(const Vector3 &other) const
{
    return Vector3(x + other.x, y + other.y, z + other.z);
}

Vector3 Vector3::operator-(const Vector3 &other) const
{
    return Vector3(x - other.x, y - other.y, z - other.z);
}

Vector3 Vector3::operator*(float scalar) const
{
    return Vector3(x * scalar, y * scalar, z * scalar);
}

Vector3 Vector3::clamp_vec(const Vector3 &p_min, const Vector3 &p_max) const
{
    return Vector3(
        clamp(x, p_min.x, p_max.x),
        clamp(y, p_min.y, p_max.y),
        clamp(z, p_min.z, p_max.z));
}

float Vector3::length() const
{
    return glm::length(to_glm_vec3());
}

Vector3 Vector3::normalize() const
{
    float len = length();
    return len != 0 ? *this * (1.0f / len) : Vector3(0, 0, 0);
}

std::string Vector3::to_str() const
{
    std::stringstream ss;
    ss << "(" << x << ", " << y << ", " << z << ")";
    return ss.str();
}

float Math::sqrt(float x) { return std::sqrt(x); }
float Math::abs(float x) { return std::abs(x); }
glm::vec3 Math::normalize_3d(const glm::vec3 &vector) { return glm::normalize(vector); }
glm::vec3 Math::calculate_normal_3d(const glm::vec3 &x, const glm::vec3 &y, const glm::vec3 &z)
{
    return glm::normalize(glm::cross(x - y, z - y));
}
float Math::clamp(float number, float min_val, float max_val)
{
    return std::max(min_val, std::min(number, max_val));
}
float Math::deg_to_rad(float a) { return a * PI / 180; }
float Math::rad_to_deg(float a) { return a * 180 / PI; }
float Math::sin(float a) { return std::sin(a); }
float Math::cos(float a) { return std::cos(a); }
float Math::tan(float a) { return std::tan(a); }
float Math::atan(float y, float x) { return std::atan2(y, x); }
float Math::acos(float a) { return std::acos(a); }
float Math::asin(float a) { return std::asin(a); }
float Math::floor(float x) { return std::floor(x); }
float Math::ceil(float x) { return std::ceil(x); }
float Math::fract(float x) { return x - std::floor(x); }
float Math::mix(float a, float b, float t) { return a * (1 - t) + b * t; }
float Math::step(float edge, float x) { return x >= edge ? 1.0f : 0.0f; }
float Math::smoothstep(float edge0, float edge1, float x)
{
    float t = clamp((x - edge0) / (edge1 - edge0), 0.0f, 1.0f);
    return t * t * (3 - 2 * t);
}
float Math::lerp(float a, float b, float t) { return a * (1 - t) + b * t; }
float Math::distance_2d(const glm::vec2 &veca, const glm::vec2 &vecb) { return glm::length(veca - vecb); }
float Math::distance_3d(const glm::vec3 &veca, const glm::vec3 &vecb) { return glm::length(veca - vecb); }

Matrix4x4::Matrix4x4()
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            if (i == j)
                m[i][j] = 1.0f;
            else
                m[i][j] = 0.0f;
        }
    }
}

Matrix4x4::Matrix4x4(const float data[16])
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            m[i][j] = data[i * 4 + j];
        }
    }
}

Vector3 Matrix4x4::operator*(const Vector3 &vec) const
{
    float x = m[0][0] * vec.x + m[0][1] * vec.y + m[0][2] * vec.z + m[0][3];
    float y = m[1][0] * vec.x + m[1][1] * vec.y + m[1][2] * vec.z + m[1][3];
    float z = m[2][0] * vec.x + m[2][1] * vec.y + m[2][2] * vec.z + m[2][3];
    return Vector3(x, y, z);
}

Matrix4x4 Matrix4x4::operator+(const Matrix4x4 &other) const
{
    Matrix4x4 result;
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            result.m[i][j] = m[i][j] + other.m[i][j];
        }
    }
    return result;
}

Matrix4x4 Matrix4x4::operator-(const Matrix4x4 &other) const
{
    Matrix4x4 result;
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            result.m[i][j] = m[i][j] - other.m[i][j];
        }
    }
    return result;
}

Matrix4x4 Matrix4x4::transpose() const
{
    Matrix4x4 result;
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            result.m[i][j] = m[j][i];
        }
    }
    return result;
}

float Matrix4x4::cofactor(int row, int col) const
{
    float sub[3][3];
    int subi = 0;
    for (int i = 0; i < 4; ++i)
    {
        if (i == row)
            continue;
        int subj = 0;
        for (int j = 0; j < 4; ++j)
        {
            if (j == col)
                continue;
            sub[subi][subj] = m[i][j];
            ++subj;
        }
        ++subi;
    }
    float det = sub[0][0] * (sub[1][1] * sub[2][2] - sub[1][2] * sub[2][1]) - sub[0][1] * (sub[1][0] * sub[2][2] - sub[1][2] * sub[2][0]) + sub[0][2] * (sub[1][0] * sub[2][1] - sub[1][1] * sub[2][0]);
    return ((row + col) % 2 == 0 ? 1.0f : -1.0f) * det;
}

float Matrix4x4::determinant() const
{
    return m[0][0] * cofactor(0, 0) - m[0][1] * cofactor(0, 1) + m[0][2] * cofactor(0, 2) - m[0][3] * cofactor(0, 3);
}

Matrix4x4 Matrix4x4::inverse() const
{
    float det = determinant();
    assert(det != 0.0f && "Determinant is zero, matrix is not invertible!");
    float invDet = 1.0f / det;

    Matrix4x4 adjoint;
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            adjoint.m[i][j] = cofactor(i, j);
        }
    }

    adjoint = adjoint.transpose();
    Matrix4x4 result;
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            result.m[i][j] = adjoint.m[i][j] * invDet;
        }
    }
    return result;
}

void Matrix4x4::print() const
{
    for (int i = 0; i < 4; ++i)
    {
        for (int j = 0; j < 4; ++j)
        {
            std::cout << m[i][j] << " ";
        }
        std::cout << std::endl;
    }
}

Matrix4x4 Matrix4x4::identity()
{
    Matrix4x4 result;
    return result;
}

Matrix4x4 Matrix4x4::translation(const Vector3 &translation)
{
    Matrix4x4 result = Matrix4x4::identity();
    result.m[0][3] = translation.x;
    result.m[1][3] = translation.y;
    result.m[2][3] = translation.z;
    return result;
}

Matrix4x4 Matrix4x4::rotation_x(float angle)
{
    Matrix4x4 result = Matrix4x4::identity();
    float cos_angle = cos(angle);
    float sin_angle = sin(angle);
    result.m[1][1] = cos_angle;
    result.m[1][2] = -sin_angle;
    result.m[2][1] = sin_angle;
    result.m[2][2] = cos_angle;
    return result;
}

Matrix4x4 Matrix4x4::rotation_y(float angle)
{
    Matrix4x4 result = Matrix4x4::identity();
    float cos_angle = cos(angle);
    float sin_angle = sin(angle);
    result.m[0][0] = cos_angle;
    result.m[0][2] = sin_angle;
    result.m[2][0] = -sin_angle;
    result.m[2][2] = cos_angle;
    return result;
}

Matrix4x4 Matrix4x4::rotation_z(float angle)
{
    Matrix4x4 result = Matrix4x4::identity();
    float cos_angle = cos(angle);
    float sin_angle = sin(angle);
    result.m[0][0] = cos_angle;
    result.m[0][1] = -sin_angle;
    result.m[1][0] = sin_angle;
    result.m[1][1] = cos_angle;
    return result;
}

Matrix4x4 Matrix4x4::scale(const Vector3 &scale)
{
    Matrix4x4 result = Matrix4x4::identity();
    result.m[0][0] = scale.x;
    result.m[1][1] = scale.y;
    result.m[2][2] = scale.z;
    return result;
}

float Matrix4x4::determinant_3x3() const
{
    return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
           m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
           m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
}

PYBIND11_MODULE(Math, m)
{
    py::class_<Vector2>(m, "Vector2")
        .def(py::init<float, float>())
        .def("__add__", &Vector2::operator+)
        .def("__sub__", &Vector2::operator-)
        .def("__mul__", &Vector2::operator*)
        .def("length", &Vector2::length)
        .def("normalize", &Vector2::normalize)
        .def("to_str", &Vector2::to_str)
        .def("clamp", &Vector2::clamp_vec);

    py::class_<Vector3>(m, "Vector3")
        .def(py::init<float, float, float>())
        .def("__add__", &Vector3::operator+)
        .def("__sub__", &Vector3::operator-)
        .def("__mul__", &Vector3::operator*)
        .def("length", &Vector3::length)
        .def("normalize", &Vector3::normalize)
        .def("to_str", &Vector3::to_str)
        .def("clamp", &Vector3::clamp_vec);

    m.def("sqrt", &Math::sqrt, py::arg("x"), "Calculate the square root of a number");
    m.def("abs", &Math::abs, py::arg("x"), "Calculate the absolute value of a number");
    m.def("normalize_3d", &Math::normalize_3d, py::arg("vector"), "Normalize a 3D vector");
    m.def("calculate_normal_3d", &Math::calculate_normal_3d, py::arg("x"), py::arg("y"), py::arg("z"), "Calculate the normal of a triangle given three 3D vectors");
    m.def("clamp", &Math::clamp, py::arg("val"), py::arg("min_val"), py::arg("max_val"), "Clamp a number between a min and max value");
    m.def("deg_to_rad", &Math::deg_to_rad, py::arg("a"), "Convert degrees to radians");
    m.def("rad_to_deg", &Math::rad_to_deg, py::arg("a"), "Convert radians to degrees");
    m.def("sin", &Math::sin, py::arg("a"), "Calculate the sine of a number");
    m.def("cos", &Math::cos, py::arg("a"), "Calculate the cosine of a number");
    m.def("tan", &Math::tan, py::arg("a"), "Calculate the tangent of a number");
    m.def("atan", &Math::atan, py::arg("y"), py::arg("x"), "Calculate the arctangent of a number");
    m.def("acos", &Math::acos, py::arg("a"), "Calculate the arccosine of a number");
    m.def("asin", &Math::asin, py::arg("a"), "Calculate the arcsine of a number");
    m.def("floor", &Math::floor, py::arg("x"), "Calculate the floor of a number");
    m.def("ceil", &Math::ceil, py::arg("x"), "Calculate the ceiling of a number");
    m.def("fract", &Math::fract, py::arg("x"), "Get the fractional part of a number");
    m.def("mix", &Math::mix, py::arg("a"), py::arg("b"), py::arg("t"), "Linearly interpolate between two numbers");
    m.def("step", &Math::step, py::arg("edge"), py::arg("x"), "Step function: returns 0.0f if x < edge, else 1.0f");
    m.def("smoothstep", &Math::smoothstep, py::arg("edge0"), py::arg("edge1"), py::arg("x"), "Smoothstep function: smoother interpolation between 0 and 1");
    m.def("lerp", &Math::lerp, py::arg("a"), py::arg("b"), py::arg("t"), "Linear interpolation between two numbers");
    m.def("distance_2d", &Math::distance_2d, py::arg("veca"), py::arg("vecb"), "Calculate the distance between two points");
    m.def("distance_3d", &Math::distance_3d, py::arg("veca"), py::arg("vecb"), "Calculate the distance between two points");
}

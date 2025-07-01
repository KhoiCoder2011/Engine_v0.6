#ifndef MATH_H
#define MATH_H

#include <glm/glm.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

class Math
{
public:
    static float sqrt(float x);
    static float abs(float x);
    static glm::vec3 normalize_3d(const glm::vec3 &vector);
    static glm::vec3 calculate_normal_3d(const glm::vec3 &x, const glm::vec3 &y, const glm::vec3 &z);
    static float clamp(float number, float min_val, float max_val);
    static float deg_to_rad(float a);
    static float rad_to_deg(float a);
    static float sin(float a);
    static float cos(float a);
    static float tan(float a);
    static float atan(float y, float x);
    static float acos(float a);
    static float asin(float a);
    static float floor(float x);
    static float ceil(float x);
    static float fract(float x);
    static float mix(float a, float b, float t);
    static float step(float edge, float x);
    static float smoothstep(float edge0, float edge1, float x);
    static float lerp(float a, float b, float t);
    static float distance_2d(const glm::vec2 &veca, const glm::vec2 &vecb);
    static float distance_3d(const glm::vec3 &veca, const glm::vec3 &vecb);
};

class Vector2
{
public:
    float x, y;
    Vector2() : x(0.0f), y(0.0f) {}
    Vector2(float x, float y);

    glm::vec2 to_glm_vec2() const;

    Vector2 operator+(const Vector2 &other) const;
    Vector2 operator-(const Vector2 &other) const;
    Vector2 operator*(float scalar) const;
    float length() const;
    Vector2 normalize() const;
    std::string to_str() const;
    Vector2 clamp_vec(const Vector2& p_min, const Vector2& p_max) const;
};

class Vector3
{
public:
    float x, y, z;
    Vector3() : x(0.0f), y(0.0f), z(0.0f) {}
    Vector3(float x, float y, float z);

    glm::vec3 to_glm_vec3() const;

    Vector3 operator+(const Vector3 &other) const;
    Vector3 operator-(const Vector3 &other) const;
    Vector3 operator*(float scalar) const;
    float length() const;
    Vector3 normalize() const;
    std::string to_str() const;
    Vector3 clamp_vec(const Vector3& p_min, const Vector3& p_max) const;
};

class Matrix4x4
{
public:
    float m[4][4];

    Matrix4x4();
    Matrix4x4(const float data[16]);

    Vector3 operator*(const Vector3 &vec) const;
    Matrix4x4 operator+(const Matrix4x4 &other) const;
    Matrix4x4 operator-(const Matrix4x4 &other) const;
    Matrix4x4 transpose() const;
    Matrix4x4 inverse() const;
    void print() const;
    static Matrix4x4 identity();
    static Matrix4x4 translation(const Vector3 &translation);
    static Matrix4x4 rotation_x(float angle);
    static Matrix4x4 rotation_y(float angle);
    static Matrix4x4 rotation_z(float angle);
    float cofactor(int row, int col) const;
    float determinant() const;
    float determinant_3x3() const;
    static Matrix4x4 scale(const Vector3 &scale);
};

#endif

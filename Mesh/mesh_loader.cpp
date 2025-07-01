#define TINYOBJLOADER_IMPLEMENTATION
#include "tinyobjloader/tiny_obj_loader.h"
#include <iostream>
#include <vector>
#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace std;

struct Vertex
{
    float x, y, z;
    float nx, ny, nz;
    float u, v;
};

bool load_obj(const string &filepath,
              vector<Vertex> &out_vertices,
              vector<unsigned int> &out_indices)
{

    tinyobj::attrib_t attrib;
    vector<tinyobj::shape_t> shapes;
    vector<tinyobj::material_t> materials;
    string warn, err;

    bool success = tinyobj::LoadObj(&attrib, &shapes, &materials, &warn, &err, filepath.c_str());

    if (!warn.empty())
        cout << "Warning: " << warn << endl;
    if (!err.empty())
        cerr << "Error: " << err << endl;
    if (!success)
    {
        cerr << "Failed to load OBJ file." << endl;
        return false;
    }

    for (const auto &shape : shapes)
    {
        for (const auto &index : shape.mesh.indices)
        {
            Vertex vertex = {};

            if (index.vertex_index >= 0)
            {
                vertex.x = attrib.vertices[3 * index.vertex_index + 0];
                vertex.y = attrib.vertices[3 * index.vertex_index + 1];
                vertex.z = attrib.vertices[3 * index.vertex_index + 2];
            }

            if (index.texcoord_index >= 0)
            {
                vertex.u = attrib.texcoords[2 * index.texcoord_index + 0];
                vertex.v = attrib.texcoords[2 * index.texcoord_index + 1];
            }

            if (index.normal_index >= 0)
            {
                vertex.nx = attrib.normals[3 * index.normal_index + 0];
                vertex.ny = attrib.normals[3 * index.normal_index + 1];
                vertex.nz = attrib.normals[3 * index.normal_index + 2];
            }

            out_vertices.push_back(vertex);
            out_indices.push_back(static_cast<unsigned int>(out_vertices.size() - 1));
        }
    }

    return true;
}

PYBIND11_MODULE(mesh_loader, m)
{
    py::class_<Vertex>(m, "Vertex")
        .def(py::init<>())
        .def_readwrite("x", &Vertex::x)
        .def_readwrite("y", &Vertex::y)
        .def_readwrite("z", &Vertex::z)
        .def_readwrite("nx", &Vertex::nx)
        .def_readwrite("ny", &Vertex::ny)
        .def_readwrite("nz", &Vertex::nz)
        .def_readwrite("u", &Vertex::u)
        .def_readwrite("v", &Vertex::v);

    m.def("load_obj", [](const std::string &filepath)
          {
        std::vector<Vertex> vertices;
        std::vector<unsigned int> indices;
        if (!load_obj(filepath, vertices, indices)) {
            throw std::runtime_error("Failed to load OBJ file.");
        }
        return std::make_pair(vertices, indices); }, "Load an OBJ file and return a tuple (vertices, indices)");
}
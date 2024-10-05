#include "Terrain.h"

Terrain::Terrain(Window* window):
  Component(window),
  _terrainShader("heightmap.vert", "heightmap.frag")
{}

int Terrain::loadTexture(const std::string& path) {
  auto insertRes = _textureIds.insert(std::pair< std::string, int >(path, (int)_textures.size()));

  // The path was newly added
  if (insertRes.second) {
    Texture texture(path);

    SCOPE_BIND(texture)

    glGenerateMipmap(GL_TEXTURE_2D);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

    _textures.push_back(std::move(texture));

    return (int)_textures.size() - 1;
  }
  else {
    // return the current existing texture index
    return insertRes.first->second;
  }
}

const Texture* Terrain::getTexture(int index) const {
  return index < 0 || index >= _textures.size() ? nullptr : &_textures[index];
}

bool Terrain::teleportPositionOnOtherSideIfOutside(glm::vec2& position) const {
  glm::vec2 maxCoordinates = getMaxCoordinates();

  bool teleported = false;

  if (position.x < 0.f) {
    position.x += maxCoordinates.x;
    teleported = true;
  }
  else if (position.x > maxCoordinates.x) {
    position.x -= maxCoordinates.x;
    teleported = true;
  }
  if (position.y < 0.f) {
    position.y += maxCoordinates.y;
    teleported = true;
  }
  else if (position.y > maxCoordinates.y) {
    position.y -= maxCoordinates.y;
    teleported = true;
  }

  return teleported;
}

void Terrain::pythonBindings(py::module& m) {
  py::class_<Terrain, std::shared_ptr<Terrain>, Component>(m, "Terrain")
    .def("loadTexture", &Terrain::loadTexture)
    .def_readwrite("wireframe", &Terrain::_wireframe)
    .def_property_readonly("maxCoord", &Terrain::getMaxCoordinates)
    .def("isOutsideBounds", &Terrain::isOutsideBounds)
    .def("getHeight", &Terrain::getHeight)
    .def("setHeight", &Terrain::setHeight)
    .def("getTextureID", &Terrain::getTextureID)
    .def("setTextureID", &Terrain::setTextureID)
    .def("getColor", &Terrain::getColor)
    .def("setColor", &Terrain::setColor)
    .def("isNavigable", &Terrain::getIsNavigable)
    .def("setIsNavigable", &Terrain::setIsNavigable);
}


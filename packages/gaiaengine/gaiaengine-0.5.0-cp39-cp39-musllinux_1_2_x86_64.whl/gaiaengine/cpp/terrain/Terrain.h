#pragma once

#include "Color.h"
#include "Component.h"
#include "Shader.h"
#include "Texture.h"

#include <unordered_map>
#include <vector>

class Terrain : public Component {
public:
  Terrain(Window* window);
  Terrain(Terrain const&) = delete;
  Terrain& operator=(Terrain const&) = delete;
  Terrain(Terrain&& other) = default;
  Terrain& operator=(Terrain&& other) = default;
  virtual ~Terrain() = default;

  // Returns the index that is associated with the texture path. Loads the texture if necessary
  int loadTexture(const std::string& path);
  const Texture* getTexture(int index) const;
  inline void bindTexture(int index) const { if (getTexture(index)) getTexture(index)->bind(); else Texture::unbind(); }

  virtual glm::vec2 getMaxCoordinates() const = 0;
  inline bool isOutsideBounds(const glm::vec2& pos) const {
    return pos.x < 0.f || pos.y < 0.f || pos.x >= getMaxCoordinates().x || pos.y >= getMaxCoordinates().y;
  }

  // Returns whether the position was actually updated or not
  bool teleportPositionOnOtherSideIfOutside(glm::vec2& position) const;

  virtual bool getIsNavigable(const glm::vec2& position) const = 0;
  virtual void setIsNavigable(const glm::ivec2& coordinates, bool isNavigable) = 0;

  virtual float getHeight(const glm::vec2& position) const = 0;
  virtual void setHeight(const glm::ivec2& coordinates, float height) = 0;

  virtual int getTextureID(const glm::vec2& position) const = 0;
  virtual void setTextureID(const glm::ivec2& coordinates, int textureID) = 0;

  virtual Color getColor(const glm::vec2& position) const = 0;
  virtual void setColor(const glm::ivec2& coordinates, const Color& color) = 0;

  static void pythonBindings(py::module& m);

protected:
  bool _wireframe = false;

  // Maps texture paths to indices in the _textureArrays array. Each new path increments the current last index
  std::unordered_map<std::string, int> _textureIds;
  std::vector<Texture> _textures;
  Shader _terrainShader;
};
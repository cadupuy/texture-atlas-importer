bl_info = {
    "name": "Import Texture Atlas",
    "blender": (2, 93, 0),
    "category": "Object",
}

import bpy
import bmesh
import json
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

class ImportTextureAtlasOperator(bpy.types.Operator):
    bl_idname = "import_texture.atlas"
    bl_label = "Import Texture Atlas"
    
    def execute(self, context):
        settings = context.scene.texture_atlas_settings
        json_path = settings.json_path
        png_path = settings.png_path
        self.import_texture_atlas(json_path, png_path)
        return {'FINISHED'}
    
    def import_texture_atlas(self, json_path, png_path):
        # Charger le fichier de configuration
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Charger l'image de texture
        texture_image = bpy.data.images.load(png_path)

        # Créer un matériau avec la texture et gérer la transparence
        material = bpy.data.materials.new(name="AtlasMaterial")
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]

        # Créer et configurer le nœud de texture
        tex_image = material.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image.image = texture_image

        # Lier la couleur de base
        material.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

        # Activer la transparence
        material.blend_method = 'BLEND'
        material.shadow_method = 'CLIP'
        bsdf.inputs['Alpha'].default_value = 1

        # Lier le canal alpha de la texture
        material.node_tree.links.new(bsdf.inputs['Alpha'], tex_image.outputs['Alpha'])

        z_index = 0

        # Facteur d'échelle pour rapprocher les plans
        scale_factor = 0.01

        # Créer des plans pour chaque élément de l'atlas
        for frame_name, frame_data in data['frames'].items():
            x, y, w, h = frame_data['frame']['x'], frame_data['frame']['y'], frame_data['frame']['w'], frame_data['frame']['h']
            source_w, source_h = frame_data['sourceSize']['w'], frame_data['sourceSize']['h']
            sprite_x, sprite_y = frame_data['spriteSourceSize']['x'], frame_data['spriteSourceSize']['y']
            
            # Créer un nouveau plan
            bpy.ops.mesh.primitive_plane_add(size=1)
            plane = bpy.context.object
            plane.name = frame_name
            
            # Redimensionner le plan selon les dimensions de la texture
            plane.scale[0] = w * scale_factor
            plane.scale[1] = h * scale_factor
            
            # Appliquer le matériau au plan
            if plane.data.materials:
                plane.data.materials[0] = material
            else:
                plane.data.materials.append(material)
            
            # Passer en mode édition pour UV mapping
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Créer une nouvelle couche d'UV
            mesh = bmesh.from_edit_mesh(plane.data)
            uv_layer = mesh.loops.layers.uv.verify()
            mesh.faces.ensure_lookup_table()
            
            # Appliquer les UVs
            uv_coords = [
                (x / texture_image.size[0], 1 - (y + h) / texture_image.size[1]),
                ((x + w) / texture_image.size[0], 1 - (y + h) / texture_image.size[1]),
                ((x + w) / texture_image.size[0], 1 - y / texture_image.size[1]),
                (x / texture_image.size[0], 1 - y / texture_image.size[1])
            ]
            
            for face in mesh.faces:
                for loop in face.loops:
                    loop[uv_layer].uv = uv_coords[loop.index % 4]

            bmesh.update_edit_mesh(plane.data)
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Calculer la position en tenant compte du trimming
            pos_x = (sprite_x + w / 2 - source_w / 2) * scale_factor
            pos_y = -(sprite_y + h / 2 - source_h / 2) * scale_factor
            
            # Positionner le plan dans la scène
            plane.location = (pos_x, pos_y, z_index * scale_factor)
            z_index += 1  # Incrémenter l'index Z pour éviter les chevauchements

        # Changer le mode d'affichage pour voir les textures
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                        break

        self.report({'INFO'}, "Importation terminée avec succès.")

class TextureAtlasSettings(bpy.types.PropertyGroup):
    png_path: StringProperty(
        name="PNG Path",
        description="Path to the PNG texture file",
        default="",
        subtype='FILE_PATH'
    )
    json_path: StringProperty(
        name="JSON Path",
        description="Path to the JSON configuration file",
        default="",
        subtype='FILE_PATH'
    )

class TextureAtlasPanel(bpy.types.Panel):
    bl_label = "Texture Atlas Importer"
    bl_idname = "OBJECT_PT_texture_atlas"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.texture_atlas_settings
        
        layout.prop(settings, "png_path")
        layout.prop(settings, "json_path")
        
        layout.operator("import_texture.atlas", text="Confirmer")

def register():
    bpy.utils.register_class(ImportTextureAtlasOperator)
    bpy.utils.register_class(TextureAtlasSettings)
    bpy.utils.register_class(TextureAtlasPanel)
    bpy.types.Scene.texture_atlas_settings = bpy.props.PointerProperty(type=TextureAtlasSettings)

def unregister():
    bpy.utils.unregister_class(ImportTextureAtlasOperator)
    bpy.utils.unregister_class(TextureAtlasSettings)
    bpy.utils.unregister_class(TextureAtlasPanel)
    del bpy.types.Scene.texture_atlas_settings

if __name__ == "__main__":
    register()

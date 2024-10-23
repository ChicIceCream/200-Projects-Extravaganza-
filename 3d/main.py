import bpy
import os
import bmesh
import math
from mathutils import Vector

def check_file_type(filepath):
    """Validate file type and existence"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
        
    valid_extensions = {
        'svg': 'vector',
        'png': 'image',
        'jpg': 'image',
        'jpeg': 'image',
        'bmp': 'image',
        'tiff': 'image'
    }
    
    ext = filepath.lower().split('.')[-1]
    if ext not in valid_extensions:
        raise ValueError(f"Unsupported file type. Supported types: {', '.join(valid_extensions.keys())}")
    
    return valid_extensions[ext]

def import_floor_plan(filepath):
    """Import 2D floor plan with appropriate method based on file type"""
    file_type = check_file_type(filepath)
    
    if file_type == 'vector':
        bpy.ops.import_curve.svg(filepath=filepath)
        # Scale SVG to reasonable size (adjust as needed)
        for obj in bpy.context.selected_objects:
            obj.scale = (0.01, 0.01, 0.01)  # Scale down SVG
            
    else:  # image
        bpy.ops.import_image.to_plane(filepath=filepath)
        # Add trace settings for image plans
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        
def setup_lighting():
    """Set up basic lighting for better visualization"""
    # Add sun light
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    
    # Add ambient light
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
    ambient = bpy.context.active_object
    ambient.data.energy = 3.0
    ambient.scale = (10, 10, 1)

def setup_camera():
    """Set up camera for rendering"""
    bpy.ops.object.camera_add(location=(10, -10, 15))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    
    # Make this the active camera
    bpy.context.scene.camera = camera

def create_materials():
    """Create basic materials for walls and roof"""
    # Wall material
    wall_mat = bpy.data.materials.new(name="Wall_Material")
    wall_mat.use_nodes = True
    wall_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
    
    # Roof material
    roof_mat = bpy.data.materials.new(name="Roof_Material")
    roof_mat.use_nodes = True
    roof_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.3, 0.3, 1)
    
    return wall_mat, roof_mat

def save_render(output_path):
    """Render and save the result"""
    # Set up rendering parameters
    bpy.context.scene.render.engine = 'CYCLES'  # Use Cycles renderer
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = True
    
    # Render and save
    bpy.context.scene.render.filepath = output_path
    bpy.ops.render.render(write_still=True)

def main(input_filepath, output_filepath="rendered_3d_model.png"):
    """Main function with visualization"""
    try:
        # Clear existing scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Import floor plan
        import_floor_plan(input_filepath)
        
        # Convert and extrude (using functions from previous script)
        convert_curves_to_mesh()
        extrude_walls()
        add_roof()
        
        # Setup visualization
        setup_lighting()
        setup_camera()
        wall_mat, roof_mat = create_materials()
        
        # Apply materials
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                if 'roof' in obj.name.lower():
                    obj.data.materials.append(roof_mat)
                else:
                    obj.data.materials.append(wall_mat)
        
        # Save render
        save_render(output_filepath)
        
        print(f"3D model created and rendered successfully!")
        print(f"Render saved to: {output_filepath}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_file = "your_floor_plan.svg"  # Update with your file path
    output_file = "rendered_3d_model.png"  # Where to save the render
    main(input_file, output_file)
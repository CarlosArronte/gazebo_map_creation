import bpy
import csv
from mathutils import Vector

ruta_csv = "/home/carlos/sim_ws/src/modelo_Blender/Pista/Monza_centerline.csv"

pontos_centrais = []
with open(ruta_csv, 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        try:
            if len(row) == 3:
                pontos_centrais.append(Vector((float(row[0]), float(row[1]), float(row[2]))))
            else:
                print(f"Linha ignorada (formato incorreto): {row}")
        except ValueError as e:
            print(f"Erro ao converter linha para números: {row}, Erro: {e}")

if not pontos_centrais:
    print("Erro: Nenhum ponto válido foi carregado do CSV.")
    raise ValueError("O arquivo CSV não contém dados válidos ou está vazio.")

largura_pista = 4.0
largura_borda = 0.5
altura_borda = 1

perfil_data = bpy.data.curves.new("PerfilPista", type='CURVE')
perfil_data.dimensions = '2D'
perfil_obj = bpy.data.objects.new("PerfilPista", perfil_data)
bpy.context.scene.collection.objects.link(perfil_obj)

spline_perfil = perfil_data.splines.new('POLY')
spline_perfil.points.add(4)
spline_perfil.points[0].co = (-largura_pista/2 - largura_borda, altura_borda, 0, 1)
spline_perfil.points[1].co = (-largura_pista/2, 0, 0, 1)
spline_perfil.points[2].co = (0, 0, 0, 1)
spline_perfil.points[3].co = (largura_pista/2, 0, 0, 1)
spline_perfil.points[4].co = (largura_pista/2 + largura_borda, altura_borda, 0, 1)

curva_data = bpy.data.curves.new("PistaCentral", type='CURVE')
curva_data.dimensions = '3D'
curva_obj = bpy.data.objects.new("PistaCentral", curva_data)
bpy.context.scene.collection.objects.link(curva_obj)

spline = curva_data.splines.new('BEZIER')
spline.bezier_points.add(len(pontos_centrais) - 1)

for i, ponto in enumerate(pontos_centrais):
    bezier_ponto = spline.bezier_points[i]
    bezier_ponto.co = ponto
    bezier_ponto.handle_left_type = 'AUTO'
    bezier_ponto.handle_right_type = 'AUTO'

spline.use_cyclic_u = True

curva_data.bevel_object = perfil_obj
curva_data.bevel_mode = 'OBJECT'
curva_data.fill_mode = 'FULL'
curva_data.resolution_u = 64
curva_data.resolution_v = 1

material_pista = bpy.data.materials.new(name="MaterialPista")
material_pista.diffuse_color = (0.1, 0.1, 0.1, 1)
material_borda = bpy.data.materials.new(name="MaterialBorda")
material_borda.diffuse_color = (0.8, 0.0, 0.0, 1)

curva_obj.data.materials.append(material_pista)

bpy.context.view_layer.objects.active = curva_obj
curva_obj.select_set(True)
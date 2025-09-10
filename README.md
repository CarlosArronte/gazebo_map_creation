# Geração de mapas para Gazebo usando Blender

## Etápas

* Abrir Blender e ir pra aba Scripting
* Click em New
* Copiar e colar o conteudo de main.py no script
* Modificar a rota do arquivo csv (o arquivo csv a usar deve ter 3 colunas: x,y,z correspondentes aos pontos do centro da pista em questão).
* Rodar o script

Com isso deve aparecer a pista na tela.

* Exportar o arquivo em formato .dae
* Criar a estrutura dos arquivos: 
```UML
.
├── PastaProyeto
│   ├── meshes
│   │   ├── Pista1.dae
│   │   ├── Pista2.dae
│   │   └── Pista3.dae
│   ├── model.config
│   └── model.sdf
└── worlds
    └── pista.world

```
IMPORTANTE: a pasta **meshes** deve de chamarse assim e conter os .dae

* Copiar o arquivo .dae para a pasta **meshes**
* O conteudo de model.config:
```python
<?xml version="1.0"?>
<model>
  <name>PistaName</name>
  <version>1.0</version>
  <sdf version="1.7">model.sdf</sdf>
  <author>
    <name>Your Name</name>
    <email>seu@email.com</email>
  </author>
  <description>Descrição da pista</description>
</model>
```
* O conteudo de model.sdf:
```python
<?xml version="1.0"?>
<sdf version="1.7">
  <model name="PistaName">
    <static>true</static>
    <link name="link">
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://PistaName/meshes/Pista3.dae</uri>
          </mesh>
        </geometry>
        <material>
          <diffuse>0.7 0.7 0.7 1</diffuse>
        </material>
      </visual>
      <collision name="collision">
        <geometry>
          <mesh>
            <uri>model://PistaName/meshes/Pista3.dae</uri>
          </mesh>
        </geometry>
      </collision>
    </link>
  </model>
</sdf>
```
* O conteudo de pista.world:
```python
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="Pista_world">
    <include>
      <uri>model://sun</uri>
    </include>
    <include>
      <uri>model://ground_plane</uri>
    </include>
    <include>
      <uri>model://PistaName</uri>
      <pose>0 0 0 0 0 0</pose>
    </include>
  </world>
</sdf>
```
IMPORTANTE: **PistaName** é apenas um nome mas deve de coincidir em todos os arquivos.

* Rodar em consola:

```cmd
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/endereço/ate/PastaProyeto
source ~/.bashrc
```
* Finalmente abrimos gazebo e a pista deve aparecer na aba **Insert**
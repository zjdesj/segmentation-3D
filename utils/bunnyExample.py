import open3d as o3d
print(o3d.__version__)


dataset = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(dataset.path)
o3d.visualization.draw_plotly([mesh], up=[0, 1, 0], front=[
                              0, 0, 1], lookat=[0.0, 0.1, 0.0], zoom=0.5)

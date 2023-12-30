import core.save_and_load.sqlWrapper as sqlWrapper
import sceneManager as sm
import mysql.connector as con


def createTables(sceneName, wrapper):
    wrapper.execute(
        "create table if not exists {0}_obj_transform(   \
            id int unsigned primary key,                \
            pos_x dec(11, 6),                            \
            pos_y dec(11, 6),                            \
            pos_z dec(11, 6),                            \
            rot_x dec(11, 6),                            \
            rot_y dec(11, 6),                            \
            rot_z dec(11, 6),                            \
            scale_x dec(11, 6),                          \
            scale_y dec(11, 6),                          \
            scale_z dec(11, 6)                           \
        )".format(
            sceneName
        )
    )

    wrapper.execute(
        "create table if not exists {0}_mesh_transform(  \
            id int unsigned primary key,                \
            pos_x dec(11, 6),                            \
            pos_y dec(11, 6),                            \
            pos_z dec(11, 6),                            \
            rot_x dec(11, 6),                            \
            rot_y dec(11, 6),                            \
            rot_z dec(11, 6),                            \
            scale_x dec(11, 6),                          \
            scale_y dec(11, 6),                          \
            scale_z dec(11, 6)                           \
        )".format(
            sceneName
        )
    )

    wrapper.execute(
        "create table if not exists {0}_textures(  \
            id int unsigned primary key,    \
            path varchar(4096)  \
        )".format(
            sceneName
        )
    )

    wrapper.execute(
        "create table if not exists {0}_vertices(    \
            id int unsigned primary key,    \
            pos_x dec(11, 6),                            \
            pos_y dec(11, 6),                            \
            pos_z dec(11, 6),                            \
            norm_x dec(11, 6),                            \
            norm_y dec(11, 6),                            \
            norm_z dec(11, 6),                            \
            tex_x dec(11, 6),                            \
            tex_y dec(11, 6)                            \
        )".format(
            sceneName
        )
    )

    wrapper.execute(
        "create table if not exists {0}_materials(    \
            id int unsigned primary key,    \
            name varchar(100),  \
            albedo_r dec(7, 6),   \
            albedo_g dec(7, 6),   \
            albedo_b dec(7, 6),   \
            emission_r dec(9, 6),   \
            emission_g dec(9, 6),   \
            emission_b dec(9, 6),   \
            roughness dec(4, 3),    \
            metallic dec(4, 3), \
            reflectance dec(4, 3),  \
            opacity dec(4, 3),  \
            texture int unsigned,    \
            roughness_map int unsigned,  \
            metallic_map int unsigned,   \
            emissive_map int unsigned,   \
            normal_map int unsigned, \
            opacity_map int unsigned,    \
            specular_map int unsigned,   \
            displacement_map int unsigned,    \
            foreign key(texture) references {0}_textures(id),   \
            foreign key(roughness_map) references {0}_textures(id),   \
            foreign key(metallic_map) references {0}_textures(id),   \
            foreign key(emissive_map) references {0}_textures(id),   \
            foreign key(normal_map) references {0}_textures(id),   \
            foreign key(opacity_map) references {0}_textures(id),   \
            foreign key(specular_map) references {0}_textures(id),   \
            foreign key(displacement_map) references {0}_textures(id)   \
        )".format(
            sceneName
        )
    )

    wrapper.execute(
        "create table if not exists {0}_meshes(  \
            id int unsigned primary key,    \
            name varchar(100),  \
            vertices_start int unsigned,    \
            vertices_count int unsigned,    \
            transform_id int unsigned,  \
            material_id int unsigned,   \
            foreign key(transform_id) references {0}_mesh_transform(id), \
            foreign key(vertices_start) references {0}_vertices(id),  \
            foreign key(material_id) references {0}_materials(id)    \
        )".format(
            sceneName
        )
    )

    wrapper.execute(
        "create table if not exists {0}_objects(                        \
            id int unsigned primary key,                                \
            name varchar(100),                                          \
            meshes_start int unsigned,                                  \
            meshes_count int unsigned,                                  \
            transform_id int unsigned,                                  \
            foreign key(transform_id) references {0}_obj_transform(id), \
            foreign key(meshes_start) references {0}_meshes(id)           \
        )".format(
            sceneName
        )
    )


def save():
    wrapper = sm.currentScene.sqlWrapper
    sceneName = sm.currentScene.name

    # if not sm.currentScene.saved:
    #     wrapper.execute("insert into scenes values('{}')".format(sceneName))

    createTables(sceneName, wrapper)

    wrapper.execute("delete from {}_objects".format(sceneName))
    wrapper.execute("delete from {}_meshes".format(sceneName))
    wrapper.execute("delete from {}_materials".format(sceneName))
    wrapper.execute("delete from {}_vertices".format(sceneName))
    wrapper.execute("delete from {}_textures".format(sceneName))
    wrapper.execute("delete from {}_obj_transform".format(sceneName))
    wrapper.execute("delete from {}_mesh_transform".format(sceneName))

    # Object transforms
    for i, t in enumerate(sm.currentScene.sceneRenderer.objectTransforms):
        valueStr = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            i, *t.position, *t.rotation, *t.scale
        )
        wrapper.execute(
            "insert into {0}_obj_transform values({1})".format(sceneName, valueStr)
        )

    # Mesh transforms
    for i, t in enumerate(sm.currentScene.sceneRenderer.meshTransforms):
        valueStr = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            i, *t.position, *t.rotation, *t.scale
        )
        wrapper.execute(
            "insert into {0}_mesh_transform values({1})".format(sceneName, valueStr)
        )

    # Textures
    for i, tex in enumerate(sm.currentScene.sceneRenderer.texPaths):
        valueStr = "{}, '{}'".format(i, tex)
        wrapper.execute(
            "insert into {0}_textures values({1})".format(sceneName, valueStr)
        )

    # Vertices
    # for i, v in enumerate(sm.currentScene.sceneRenderer.vertices):
    #     valueStr = "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
    #         i, *v.position[:-1], *v.normal[:-1], *v.textureCoord
    #     )
    #     wrapper.execute(
    #         "insert into {0}_vertices values({1})".format(sceneName, valueStr)
    #     )

    # Vertices
    vertices = sm.currentScene.sceneRenderer.vertices
    valuesList = [
        "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(
            i, *v.position[:-1], *v.normal[:-1], *v.textureCoord
        )
        for i, v in enumerate(vertices)
    ]

    query = "insert into {0}_vertices values({1})"
    [wrapper.execute(query.format(sceneName, i)) for i in valuesList]


    # Materials
    for i, mat in enumerate(sm.currentScene.sceneRenderer.materials):
        valueStr = ("{},'{}'," + "{}," * 18)[:-1].format(
            i,
            sm.currentScene.sceneRenderer.matNames[i],
            *mat.albedo[:-1],
            *mat.emission[:-1],
            mat.roughness[0],
            mat.metallic,
            mat.reflectance,
            mat.opacity,
            mat.textureID if mat.textureID != -1 else "null",
            mat.roughnessMapID if mat.roughnessMapID != -1 else "null",
            mat.metallicMapID if mat.metallicMapID != -1 else "null",
            mat.emissiveMapID if mat.emissiveMapID != -1 else "null",
            mat.normalMapID if mat.normalMapID != -1 else "null",
            mat.opacityMapID if mat.opacityMapID != -1 else "null",
            mat.specularMapID if mat.specularMapID != -1 else "null",
            mat.displacementMapID if mat.displacementMapID != -1 else "null"
        )
        wrapper.execute(
            "insert into {0}_materials values({1})".format(sceneName, valueStr)
        )

    # Meshes
    for i, mesh in enumerate(sm.currentScene.sceneRenderer.meshes):
        valueStr = "{}, '{}', {}, {}, {}, {}".format(
            i,
            sm.currentScene.sceneRenderer.meshNames[i],
            mesh.startingVertex,
            mesh.numTriangles,
            i,
            mesh.materialID,
        )
        wrapper.execute(
            "insert into {0}_meshes values({1})".format(sceneName, valueStr)
        )

    # Objects
    for i, obj in enumerate(sm.currentScene.sceneRenderer.objects):
        valueStr = "{}, '{}', {}, {}, {}".format(
            i,
            sm.currentScene.sceneRenderer.objectNames[i],
            obj.startingMesh,
            obj.numMeshes,
            i,
        )
        wrapper.execute(
            "insert into {0}_objects values({1})".format(sceneName, valueStr)
        )

    wrapper.execute("commit")

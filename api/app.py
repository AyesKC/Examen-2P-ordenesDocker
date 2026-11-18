from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import pymssql 

load_dotenv()

app = Flask(__name__)

DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("SA_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():
    return pymssql.connect(
        server=DB_SERVER,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def actualizar_total_orden(orden_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ordenes
        SET total = ISNULL(
            (
                SELECT SUM(subtotal)
                FROM orden_detalle
                WHERE orden_id = %s
            ), 0
        )
        WHERE id = %s
    """, (orden_id, orden_id))

    conn.commit()
    conn.close()

@app.route('/health')
def health():
    return jsonify({
        "status": "ok"
    }), 200

@app.route('/api/ordenes')
def listar_ordenes():

    try:

        conn = get_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute("""
            SELECT *
            FROM ordenes
            ORDER BY id
        """)

        ordenes = cursor.fetchall()

        conn.close()

        return jsonify(ordenes), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/ordenes/<int:id>')
def obtener_orden(id):

    try:

        conn = get_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute("""
            SELECT *
            FROM ordenes
            WHERE id = %s
        """, (id,))

        orden = cursor.fetchone()

        conn.close()

        if orden:

            return jsonify(orden), 200

        return jsonify({
            "mensaje": "Orden no encontrada"
        }), 404

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/ordenes', methods=['POST'])
def crear_orden():

    try:

        datos = request.get_json()

        cliente = datos.get('cliente')
        estado = datos.get('estado')

        if not cliente or not estado:

            return jsonify({
                "mensaje": "Cliente y estado son obligatorios"
            }), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO ordenes(cliente, estado, total)
            VALUES(%s, %s, 0)
        """, (cliente, estado))

        conn.commit()

        conn.close()

        return jsonify({
            "mensaje": "Orden creada correctamente"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500    

@app.route('/api/ordenes/<int:id>', methods=['PUT'])
def actualizar_orden(id):

    try:

        datos = request.get_json()

        cliente = datos.get('cliente')
        estado = datos.get('estado')

        if not cliente or not estado:

            return jsonify({
                "mensaje": "Cliente y estado son obligatorios"
            }), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE ordenes
            SET cliente = %s,
                estado = %s
            WHERE id = %s
        """, (cliente, estado, id))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            return jsonify({
                "mensaje": "Orden no encontrada"
            }), 404

        conn.close()

        return jsonify({
            "mensaje": "Orden actualizada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/ordenes/<int:id>', methods=['DELETE'])
def eliminar_orden(id):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM orden_detalle
            WHERE orden_id = %s
        """, (id,))

        cursor.execute("""
            DELETE FROM ordenes
            WHERE id = %s
        """, (id,))

        conn.commit()

        if cursor.rowcount == 0:

            conn.close()

            return jsonify({
                "mensaje": "Orden no encontrada"
            }), 404

        conn.close()

        return jsonify({
            "mensaje": "Orden eliminada correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500  

@app.route('/api/ordenes/<int:id>/detalles')
def obtener_detalles(id):

    try:

        conn = get_connection()
        cursor = conn.cursor(as_dict=True)

        cursor.execute("""
            SELECT *
            FROM orden_detalle
            WHERE orden_id = %s
            ORDER BY id
        """, (id,))

        detalles = cursor.fetchall()

        conn.close()

        return jsonify(detalles), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/ordenes/<int:id>/detalles', methods=['POST'])
def agregar_detalle(id):

    try:

        datos = request.get_json()

        producto = datos.get('producto')
        cantidad = datos.get('cantidad')
        precio_unitario = datos.get('precio_unitario')

        if not producto or not cantidad or not precio_unitario:

            return jsonify({
                "mensaje": "Todos los campos son obligatorios"
            }), 400

        subtotal = cantidad * precio_unitario

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orden_detalle
            (
                orden_id,
                producto,
                cantidad,
                precio_unitario,
                subtotal
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
        """, (
            id,
            producto,
            cantidad,
            precio_unitario,
            subtotal
        ))

        conn.commit()
        conn.close()

        actualizar_total_orden(id)

        return jsonify({
            "mensaje": "Detalle agregado correctamente"
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500  

@app.route('/api/detalles/<int:id>', methods=['PUT'])
def actualizar_detalle(id):

    try:

        datos = request.get_json()

        producto = datos.get('producto')
        cantidad = datos.get('cantidad')
        precio_unitario = datos.get('precio_unitario')

        if not producto or not cantidad or not precio_unitario:

            return jsonify({
                "mensaje": "Todos los campos son obligatorios"
            }), 400

        subtotal = cantidad * precio_unitario

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT orden_id
            FROM orden_detalle
            WHERE id = %s
        """, (id,))

        fila = cursor.fetchone()

        if not fila:

            conn.close()

            return jsonify({
                "mensaje": "Detalle no encontrado"
            }), 404

        orden_id = fila[0]

        cursor.execute("""
            UPDATE orden_detalle
            SET producto = %s,
                cantidad = %s,
                precio_unitario = %s,
                subtotal = %s
            WHERE id = %s
        """, (
            producto,
            cantidad,
            precio_unitario,
            subtotal,
            id
        ))

        conn.commit()
        conn.close()

        actualizar_total_orden(orden_id)

        return jsonify({
            "mensaje": "Detalle actualizado correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500   

@app.route('/api/detalles/<int:id>', methods=['DELETE'])
def eliminar_detalle(id):

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT orden_id
            FROM orden_detalle
            WHERE id = %s
        """, (id,))

        fila = cursor.fetchone()

        if not fila:

            conn.close()

            return jsonify({
                "mensaje": "Detalle no encontrado"
            }), 404

        orden_id = fila[0]

        cursor.execute("""
            DELETE FROM orden_detalle
            WHERE id = %s
        """, (id,))

        conn.commit()
        conn.close()

        actualizar_total_orden(orden_id)

        return jsonify({
            "mensaje": "Detalle eliminado correctamente"
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500       

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
import logging
from flask import Blueprint, request, jsonify
from infrastructure.pulsar import event_service

logger = logging.getLogger(__name__)

def create_producto_routes() -> Blueprint:
    """
    Crea las rutas para productos que usan comunicación asíncrona con Pulsar.
    """

    producto_routes = Blueprint("productos", __name__, url_prefix="/productos")

    @producto_routes.route("", methods=["GET"])
    def obtener_todos_los_productos():
        """Obtiene todos los productos usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_producto_query_all(headers=headers_dict)
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error("Timeout esperando respuesta del microservicio de productos")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de productos"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo productos: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de productos: {str(e)}"
            }), 503

    @producto_routes.route("/<string:producto_id>", methods=["GET"])
    def obtener_producto_por_id(producto_id: str):
        """Obtiene un producto por su ID usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_producto_query_by_id(
                producto_id=producto_id, 
                headers=headers_dict
            )
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error(f"Timeout esperando respuesta para producto {producto_id}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de productos"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo producto {producto_id}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de productos: {str(e)}"
            }), 503

    @producto_routes.route("/categoria/<string:categoria>", methods=["GET"])
    def obtener_productos_por_categoria(categoria: str):
        """Obtiene productos por categoría usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_producto_query_by_category(
                categoria=categoria,
                headers=headers_dict
            )
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error(f"Timeout esperando respuesta para categoría {categoria}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de productos"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo productos por categoría {categoria}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de productos: {str(e)}"
            }), 503

    @producto_routes.route("/buscar", methods=["GET"])
    def buscar_productos_por_nombre():
        """Busca productos por nombre usando eventos."""
        try:
            nombre = request.args.get("nombre", "")
            if not nombre:
                return jsonify({
                    "success": False,
                    "error": "Parámetro nombre es requerido"
                }), 400
            
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_producto_search_by_name(
                nombre=nombre,
                headers=headers_dict
            )
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error(f"Timeout esperando respuesta para búsqueda de producto {nombre}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de productos"
            }), 504
            
        except Exception as e:
            logger.error(f"Error buscando productos por nombre {nombre}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de productos: {str(e)}"
            }), 503

    return producto_routes

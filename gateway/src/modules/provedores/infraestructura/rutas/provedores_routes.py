import logging
from flask import Blueprint, request, jsonify
from infrastructure.pulsar import event_service

logger = logging.getLogger(__name__)

def create_provedores_routes() -> Blueprint:
    """
    Crea las rutas para proveedores que usan comunicación asíncrona con Pulsar.
    """

    provedores_routes = Blueprint("provedores", __name__, url_prefix="/provedores")

    @provedores_routes.route("", methods=["GET"])
    def obtener_todos_los_provedores():
        """Obtiene todos los proveedores usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_provedor_query_all(headers=headers_dict)
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error("Timeout esperando respuesta del microservicio de proveedores")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de proveedores"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo proveedores: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de proveedores: {str(e)}"
            }), 503

    @provedores_routes.route("/<int:provedor_id>", methods=["GET"])
    def obtener_provedor_por_id(provedor_id: int):
        """Obtiene un proveedor por su ID usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_provedor_query_by_id(
                provedor_id=provedor_id,
                headers=headers_dict
            )
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error(f"Timeout esperando respuesta para proveedor {provedor_id}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de proveedores"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo proveedor {provedor_id}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de proveedores: {str(e)}"
            }), 503

    @provedores_routes.route("/nit/<int:nit>", methods=["GET"])
    def obtener_provedor_por_nit(nit: int):
        """Obtiene un proveedor por su NIT usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_provedor_query_by_nit(
                nit=nit,
                headers=headers_dict
            )
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error(f"Timeout esperando respuesta para NIT {nit}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de proveedores"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo proveedor por NIT {nit}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de proveedores: {str(e)}"
            }), 503

    @provedores_routes.route("/pais/<string:pais>", methods=["GET"])
    def obtener_provedores_por_pais(pais: str):
        """Obtiene proveedores por país usando eventos."""
        try:
            # Convertir headers de Flask a diccionario
            headers_dict = dict(request.headers)
            
            # Publicar evento y esperar respuesta
            response = event_service.publish_provedor_query_by_country(
                pais=pais,
                headers=headers_dict
            )
            
            # Determinar status code desde la respuesta
            status_code = response.get('status_code', 200)
            
            # Remover status_code de la respuesta antes de enviarla
            if 'status_code' in response:
                del response['status_code']
            
            return jsonify(response), status_code
            
        except TimeoutError:
            logger.error(f"Timeout esperando respuesta para país {pais}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de proveedores"
            }), 504
            
        except Exception as e:
            logger.error(f"Error obteniendo proveedores por país {pais}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de proveedores: {str(e)}"
            }), 503

    @provedores_routes.route("/buscar", methods=["GET"])
    def buscar_provedores_por_nombre():
        """Busca proveedores por nombre usando eventos."""
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
            response = event_service.publish_provedor_search_by_name(
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
            logger.error(f"Timeout esperando respuesta para búsqueda de proveedor {nombre}")
            return jsonify({
                "success": False,
                "error": "Timeout conectando con el servicio de proveedores"
            }), 504
            
        except Exception as e:
            logger.error(f"Error buscando proveedores por nombre {nombre}: {e}")
            return jsonify({
                "success": False,
                "error": f"Error conectando con el servicio de proveedores: {str(e)}"
            }), 503

    return provedores_routes

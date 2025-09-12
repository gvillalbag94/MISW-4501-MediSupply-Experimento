from typing import List, Optional
from flask import jsonify
from src.dominio.entities.provedor import Provedor
from src.aplicacion.use_cases.provedor_use_case import ProvedorUseCase
from src.aplicacion.mappers.provedor_mapper import ProvedorMapper


class ProvedorCmd:
    """Controlador para la gestión de proveedores."""
    
    def __init__(self, provedor_use_case: ProvedorUseCase):
        self.provedor_use_case = provedor_use_case
    
    def obtener_todos_los_provedores(self):
        """Obtiene todos los proveedores."""
        try:
            provedores = self.provedor_use_case.obtener_todos_los_provedores()
            provedores_dto = ProvedorMapper.entities_to_dtos(provedores)
            provedores_dict = ProvedorMapper.dtos_to_dicts(provedores_dto)
            return jsonify({
                "success": True,
                "data": provedores_dict,
                "total": len(provedores_dict)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error al obtener proveedores: {str(e)}"
            }), 500
    
    def obtener_provedor_por_id(self, provedor_id: int):
        """Obtiene un proveedor por su ID."""
        try:
            provedor = self.provedor_use_case.obtener_provedor_por_id(provedor_id)
            if not provedor:
                return jsonify({
                    "success": False,
                    "error": f"Proveedor con ID {provedor_id} no encontrado"
                }), 404
            
            provedor_dto = ProvedorMapper.entity_to_dto(provedor)
            provedor_dict = ProvedorMapper.dto_to_dict(provedor_dto)
            return jsonify({
                "success": True,
                "data": provedor_dict
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error al obtener proveedor: {str(e)}"
            }), 500
    
    def obtener_provedor_por_nit(self, nit: int):
        """Obtiene un proveedor por su NIT."""
        try:
            provedor = self.provedor_use_case.obtener_provedor_por_nit(nit)
            if not provedor:
                return jsonify({
                    "success": False,
                    "error": f"Proveedor con NIT {nit} no encontrado"
                }), 404
            
            provedor_dto = ProvedorMapper.entity_to_dto(provedor)
            provedor_dict = ProvedorMapper.dto_to_dict(provedor_dto)
            return jsonify({
                "success": True,
                "data": provedor_dict
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error al obtener proveedor: {str(e)}"
            }), 500
    
    def obtener_provedores_por_pais(self, pais: str):
        """Obtiene proveedores por país."""
        try:
            provedores = self.provedor_use_case.obtener_provedores_por_pais(pais)
            provedores_dto = ProvedorMapper.entities_to_dtos(provedores)
            provedores_dict = ProvedorMapper.dtos_to_dicts(provedores_dto)
            return jsonify({
                "success": True,
                "data": provedores_dict,
                "total": len(provedores_dict)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error al obtener proveedores: {str(e)}"
            }), 500
    
    def buscar_provedores_por_nombre(self, nombre: str):
        """Busca proveedores por nombre."""
        try:
            provedores = self.provedor_use_case.buscar_provedores_por_nombre(nombre)
            provedores_dto = ProvedorMapper.entities_to_dtos(provedores)
            provedores_dict = ProvedorMapper.dtos_to_dicts(provedores_dto)
            return jsonify({
                "success": True,
                "data": provedores_dict,
                "total": len(provedores_dict)
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Error al buscar proveedores: {str(e)}"
            }), 500

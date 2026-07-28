"""
BlueprintBot v2: Utility Service Overlays & Commercial Supply Chain Management

This module provides comprehensive utility service integration (electricity, gas, water)
and commercial supply chain management for construction projects.

Features:
- Real-time utility service mapping and overlays
- Supply chain optimization and cost management
- Vendor management and procurement automation
- Compliance and regulatory tracking

Author: BlueprintBot Team
Version: 1.0.0
"""

import logging
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UtilityType(Enum):
    """Types of utility services."""
    ELECTRICITY = "electricity"
    GAS = "gas"
    WATER = "water"
    SEWAGE = "sewage"
    TELECOMMUNICATIONS = "telecommunications"

class ComplianceStatus(Enum):
    """Compliance status levels."""
    COMPLIANT = "compliant"
    WARNING = "warning"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"

@dataclass
class UtilityService:
    """Represents a utility service connection or infrastructure."""
    service_id: str
    utility_type: UtilityType
    location: Tuple[float, float, float]
    capacity: float
    unit: str
    provider: str
    connection_status: str
    last_inspection: datetime
    next_inspection: datetime
    compliance_status: ComplianceStatus

@dataclass
class SupplierProfile:
    """Represents a commercial supplier/vendor."""
    supplier_id: str
    company_name: str
    contact_email: str
    contact_phone: str
    product_categories: List[str]
    rating: float  # 0-5
    delivery_time_days: int
    cost_per_unit: float
    minimum_order_quantity: int
    certifications: List[str]
    compliance_verified: bool

@dataclass
class ProcurementOrder:
    """Represents a procurement order."""
    order_id: str
    supplier_id: str
    product_name: str
    quantity: int
    unit_price: float
    total_cost: float
    order_date: datetime
    expected_delivery_date: datetime
    actual_delivery_date: Optional[datetime]
    status: str  # "pending", "shipped", "delivered", "cancelled"
    tracking_number: Optional[str]

class UtilityServiceManager:
    """Manages utility service overlays and integration."""
    
    def __init__(self):
        self.services = {}
        self.service_history = []
        
    def register_utility_service(self, service: UtilityService) -> None:
        """Register a utility service."""
        self.services[service.service_id] = service
        self.service_history.append({
            "action": "registered",
            "service_id": service.service_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.info(f"Registered utility service: {service.service_id}")
        
    def get_service_overlay(self, utility_type: UtilityType) -> Dict[str, Any]:
        """Get overlay data for a specific utility type."""
        services_of_type = [
            s for s in self.services.values()
            if s.utility_type == utility_type
        ]
        
        overlay_data = {
            "utility_type": utility_type.value,
            "services": [
                {
                    "id": s.service_id,
                    "location": s.location,
                    "capacity": s.capacity,
                    "unit": s.unit,
                    "provider": s.provider,
                    "status": s.connection_status,
                    "compliance": s.compliance_status.value
                }
                for s in services_of_type
            ],
            "total_capacity": sum(s.capacity for s in services_of_type),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return overlay_data
        
    def check_compliance(self, service_id: str) -> Dict[str, Any]:
        """Check compliance status of a utility service."""
        if service_id not in self.services:
            return {"error": "Service not found"}
            
        service = self.services[service_id]
        
        compliance_report = {
            "service_id": service_id,
            "utility_type": service.utility_type.value,
            "current_status": service.compliance_status.value,
            "last_inspection": service.last_inspection.isoformat(),
            "next_inspection": service.next_inspection.isoformat(),
            "days_until_inspection": (service.next_inspection - datetime.utcnow()).days,
            "recommendations": self._generate_compliance_recommendations(service)
        }
        
        return compliance_report
        
    def _generate_compliance_recommendations(self, service: UtilityService) -> List[str]:
        """Generate compliance recommendations."""
        recommendations = []
        
        if service.compliance_status == ComplianceStatus.NON_COMPLIANT:
            recommendations.append(f"URGENT: {service.utility_type.value} service is non-compliant. Immediate action required.")
        elif service.compliance_status == ComplianceStatus.WARNING:
            recommendations.append(f"WARNING: {service.utility_type.value} service has compliance issues. Schedule inspection.")
            
        days_until_inspection = (service.next_inspection - datetime.utcnow()).days
        if days_until_inspection < 7:
            recommendations.append(f"Inspection due in {days_until_inspection} days. Schedule now.")
            
        return recommendations

class SupplyChainManager:
    """Manages commercial supply chain, procurement, and vendor relationships."""
    
    def __init__(self):
        self.suppliers = {}
        self.orders = {}
        self.order_history = []
        self.cost_analytics = {}
        
    def register_supplier(self, supplier: SupplierProfile) -> None:
        """Register a new supplier."""
        self.suppliers[supplier.supplier_id] = supplier
        logger.info(f"Registered supplier: {supplier.company_name}")
        
    def get_suppliers_by_category(self, category: str) -> List[SupplierProfile]:
        """Get suppliers by product category."""
        return [
            s for s in self.suppliers.values()
            if category in s.product_categories
        ]
        
    def optimize_procurement(self, product_name: str, quantity: int) -> Dict[str, Any]:
        """Optimize procurement by finding the best supplier."""
        suitable_suppliers = [
            s for s in self.suppliers.values()
            if s.minimum_order_quantity <= quantity and s.compliance_verified
        ]
        
        if not suitable_suppliers:
            return {"error": "No suitable suppliers found"}
            
        # Score suppliers based on rating, cost, and delivery time
        scored_suppliers = []
        for supplier in suitable_suppliers:
            score = (
                (supplier.rating / 5.0) * 0.4 +  # 40% weight on rating
                (1.0 / (supplier.cost_per_unit + 1)) * 0.3 +  # 30% weight on cost
                (1.0 / (supplier.delivery_time_days + 1)) * 0.3  # 30% weight on delivery
            )
            scored_suppliers.append((supplier, score))
            
        scored_suppliers.sort(key=lambda x: x[1], reverse=True)
        best_supplier = scored_suppliers[0][0]
        
        recommendation = {
            "product": product_name,
            "quantity": quantity,
            "recommended_supplier": {
                "id": best_supplier.supplier_id,
                "name": best_supplier.company_name,
                "rating": best_supplier.rating,
                "cost_per_unit": best_supplier.cost_per_unit,
                "total_cost": best_supplier.cost_per_unit * quantity,
                "delivery_time_days": best_supplier.delivery_time_days
            },
            "alternatives": [
                {
                    "id": s[0].supplier_id,
                    "name": s[0].company_name,
                    "score": s[1]
                }
                for s in scored_suppliers[1:4]  # Top 3 alternatives
            ]
        }
        
        return recommendation
        
    def create_procurement_order(self, supplier_id: str, product_name: str, quantity: int) -> ProcurementOrder:
        """Create a procurement order."""
        if supplier_id not in self.suppliers:
            raise ValueError(f"Supplier {supplier_id} not found")
            
        supplier = self.suppliers[supplier_id]
        
        order_id = f"order_{hashlib.md5(f'{supplier_id}_{product_name}_{datetime.utcnow()}'.encode()).hexdigest()[:8]}"
        
        order = ProcurementOrder(
            order_id=order_id,
            supplier_id=supplier_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=supplier.cost_per_unit,
            total_cost=supplier.cost_per_unit * quantity,
            order_date=datetime.utcnow(),
            expected_delivery_date=datetime.utcnow() + __import__('datetime').timedelta(days=supplier.delivery_time_days),
            actual_delivery_date=None,
            status="pending",
            tracking_number=None
        )
        
        self.orders[order_id] = order
        self.order_history.append(order_id)
        
        logger.info(f"Created procurement order: {order_id}")
        
        return order
        
    def get_cost_analytics(self) -> Dict[str, Any]:
        """Generate cost analytics for all orders."""
        total_cost = sum(o.total_cost for o in self.orders.values())
        delivered_cost = sum(o.total_cost for o in self.orders.values() if o.status == "delivered")
        pending_cost = sum(o.total_cost for o in self.orders.values() if o.status == "pending")
        
        analytics = {
            "total_orders": len(self.orders),
            "total_cost": total_cost,
            "delivered_cost": delivered_cost,
            "pending_cost": pending_cost,
            "average_order_cost": total_cost / len(self.orders) if self.orders else 0,
            "orders_by_status": {
                "pending": sum(1 for o in self.orders.values() if o.status == "pending"),
                "shipped": sum(1 for o in self.orders.values() if o.status == "shipped"),
                "delivered": sum(1 for o in self.orders.values() if o.status == "delivered"),
                "cancelled": sum(1 for o in self.orders.values() if o.status == "cancelled")
            }
        }
        
        return analytics
        
    def get_supply_chain_report(self) -> str:
        """Generate a comprehensive supply chain report."""
        analytics = self.get_cost_analytics()
        
        report = f"""
# BlueprintBot V2: Supply Chain Management Report
Generated: {datetime.utcnow().isoformat()}

## Summary
- Total Suppliers: {len(self.suppliers)}
- Total Orders: {analytics['total_orders']}
- Total Procurement Cost: ${analytics['total_cost']:,.2f}
- Pending Orders Cost: ${analytics['pending_cost']:,.2f}

## Orders by Status
- Pending: {analytics['orders_by_status']['pending']}
- Shipped: {analytics['orders_by_status']['shipped']}
- Delivered: {analytics['orders_by_status']['delivered']}
- Cancelled: {analytics['orders_by_status']['cancelled']}

## Top Suppliers
"""
        
        top_suppliers = sorted(
            self.suppliers.values(),
            key=lambda s: s.rating,
            reverse=True
        )[:5]
        
        for supplier in top_suppliers:
            report += f"\n### {supplier.company_name}\n"
            report += f"- Rating: {supplier.rating}/5\n"
            report += f"- Delivery Time: {supplier.delivery_time_days} days\n"
            report += f"- Cost per Unit: ${supplier.cost_per_unit}\n"
            report += f"- Compliance: {'Verified' if supplier.compliance_verified else 'Not Verified'}\n"
            
        return report

class IntegratedServiceManager:
    """Integrates utility services and supply chain management."""
    
    def __init__(self):
        self.utility_manager = UtilityServiceManager()
        self.supply_chain_manager = SupplyChainManager()
        
    def get_integrated_report(self) -> Dict[str, Any]:
        """Generate an integrated report of utilities and supply chain."""
        return {
            "utilities": {
                "electricity": self.utility_manager.get_service_overlay(UtilityType.ELECTRICITY),
                "gas": self.utility_manager.get_service_overlay(UtilityType.GAS),
                "water": self.utility_manager.get_service_overlay(UtilityType.WATER)
            },
            "supply_chain": self.supply_chain_manager.get_cost_analytics(),
            "timestamp": datetime.utcnow().isoformat()
        }

if __name__ == "__main__":
    # Example usage
    integrated = IntegratedServiceManager()
    
    # Register utility services
    electricity = UtilityService(
        service_id="elec_001",
        utility_type=UtilityType.ELECTRICITY,
        location=(0, 0, 0),
        capacity=500,
        unit="kW",
        provider="City Power Co.",
        connection_status="active",
        last_inspection=datetime.utcnow(),
        next_inspection=datetime.utcnow(),
        compliance_status=ComplianceStatus.COMPLIANT
    )
    integrated.utility_manager.register_utility_service(electricity)
    
    # Register suppliers
    supplier = SupplierProfile(
        supplier_id="sup_001",
        company_name="BuildMaterials Inc.",
        contact_email="contact@buildmaterials.com",
        contact_phone="555-1234",
        product_categories=["concrete", "steel", "lumber"],
        rating=4.8,
        delivery_time_days=3,
        cost_per_unit=100,
        minimum_order_quantity=10,
        certifications=["ISO 9001", "ISO 14001"],
        compliance_verified=True
    )
    integrated.supply_chain_manager.register_supplier(supplier)
    
    # Get integrated report
    report = integrated.get_integrated_report()
    print(json.dumps(report, indent=2, default=str))

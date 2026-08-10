from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg, Count, Sum
from .models import *

# ============================================================
# REGISTER ALL MODELS FIRST (ensures everything appears)
# ============================================================

# List of all models to register
# NOTE: Only include models here that do NOT have a dedicated @admin.register(...)
# ModelAdmin class further down in this file. Every other model below is already
# registered via those decorators, and admin.site.register()'ing the same model
# twice raises django.contrib.admin.exceptions.AlreadyRegistered — which is NOT
# caught when the second registration happens via the @admin.register decorator,
# crashing admin.autodiscover() at Django startup (this took down the whole site,
# not just /admin/). CartItem is the only model here with no custom ModelAdmin.
models_to_register = [
    CartItem,
]

# Register each model with error handling
for model in models_to_register:
    try:
        admin.site.register(model)
    except Exception:
        pass

# ============================================================
# READATHON MODELS
# ============================================================

try:
    admin.site.register(ReadathonReport)
except Exception:
    pass

try:
    admin.site.register(InterventionNote)
except Exception:
    pass

# ============================================================
# AI E-LAB MODELS
# ============================================================

try:
    from .elab_ai_models import ELabProject, ELabMilestone, StudentAIInsight, AIChatLog
    admin.site.register(ELabProject)
    admin.site.register(ELabMilestone)
    admin.site.register(StudentAIInsight)
    admin.site.register(AIChatLog)
except ImportError:
    pass
except Exception:
    pass

# ============================================================
# 🛒 STORE ADMIN REGISTRATIONS
# ============================================================

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon_display', 'is_active', 'order', 'product_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def icon_display(self, obj):
        return obj.icon if obj.icon else '📦'
    icon_display.short_description = 'Icon'
    
    def product_count(self, obj):
        return obj.products.filter(is_active=True).count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name_display', 'sku', 'product_type_badge', 'price_display', 
        'stock_status', 'is_active_badge', 'is_featured_badge'
    ]
    list_filter = ['product_type', 'is_active', 'is_featured', 'is_best_seller', 'categories']
    search_fields = ['name', 'sku', 'description']
    readonly_fields = ['slug', 'sku', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'sku', 'product_type', 'categories')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'specifications')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost')
        }),
        ('Inventory', {
            'fields': ('stock', 'low_stock_threshold', 'is_in_stock', 'allow_backorder')
        }),
        ('Media', {
            'fields': ('main_image', 'images')
        }),
        ('Additional', {
            'fields': ('age_group', 'difficulty_level', 'includes', 'requirements', 'xp_reward')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_best_seller', 'is_active', 'is_digital', 'digital_file')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description')
        }),
        ('Shipping', {
            'fields': ('weight',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def name_display(self, obj):
        return format_html('<strong>{}</strong>', obj.name[:40])
    name_display.short_description = 'Name'
    
    def price_display(self, obj):
        if obj.compare_price and obj.compare_price > obj.price:
            return format_html(
                '<span style="color:#DC2626;font-weight:bold;">KES {}</span> '
                '<span style="text-decoration:line-through;color:#9CA3AF;">KES {}</span>',
                obj.price, obj.compare_price
            )
        return format_html('<span style="font-weight:bold;">KES {}</span>', obj.price)
    price_display.short_description = 'Price'
    
    def product_type_badge(self, obj):
        colors = {
            'science_kit': '#16A34A',
            'electronics': '#3B82F6',
            'book': '#8B5CF6',
            'merchandise': '#F59E0B',
            'digital': '#EC4899',
            'robotics_kit': '#DC2626',
        }
        color = colors.get(obj.product_type, '#6B7280')
        label = dict(Product.PRODUCT_TYPES).get(obj.product_type, obj.product_type)
        return format_html(
            '<span style="background:{}20;color:{};padding:2px 10px;border-radius:12px;font-size:0.7rem;">{}</span>',
            color, color, label
        )
    product_type_badge.short_description = 'Type'
    
    def stock_status(self, obj):
        if obj.stock <= 0:
            if obj.allow_backorder:
                return format_html('<span style="color:#F59E0B;">⏳ Backorder</span>')
            return format_html('<span style="color:#DC2626;">❌ Out of Stock</span>')
        elif obj.stock <= obj.low_stock_threshold:
            return format_html('<span style="color:#F59E0B;">⚠️ Low Stock ({})</span>', obj.stock)
        return format_html('<span style="color:#16A34A;">✅ In Stock ({})</span>', obj.stock)
    stock_status.short_description = 'Stock'
    
    def is_active_badge(self, obj):
        return format_html(
            '<span style="color:{};">●</span> {}',
            '#16A34A' if obj.is_active else '#DC2626',
            'Active' if obj.is_active else 'Inactive'
        )
    is_active_badge.short_description = 'Status'
    
    def is_featured_badge(self, obj):
        return '⭐' if obj.is_featured else '—'
    is_featured_badge.short_description = 'Featured'


# ============================================================
# MARITIME ACADEMY ADMIN
# ============================================================
try:
    from .maritime_models import MaritimeCourse, MaritimeMaterial, MaritimeSession, MaritimeEnrollment

    try:
        admin.site.unregister(MaritimeCourse)
    except Exception:
        pass

    @admin.register(MaritimeCourse)
    class MaritimeCourseAdmin(admin.ModelAdmin):
        list_display = ['code', 'title', 'track', 'is_published', 'created_at']
        list_filter = ['track', 'is_published']
        search_fields = ['code', 'title']
        prepopulated_fields = {'slug': ('title',)}

    try:
        admin.site.unregister(MaritimeMaterial)
    except Exception:
        pass

    @admin.register(MaritimeMaterial)
    class MaritimeMaterialAdmin(admin.ModelAdmin):
        list_display = ['title', 'course', 'file_type', 'uploaded_by', 'created_at']
        list_filter = ['file_type', 'created_at']
        search_fields = ['title', 'course__title']

    try:
        admin.site.unregister(MaritimeSession)
    except Exception:
        pass

    @admin.register(MaritimeSession)
    class MaritimeSessionAdmin(admin.ModelAdmin):
        list_display = ['title', 'course', 'start_time', 'is_recurring']
        list_filter = ['start_time', 'is_recurring']
        search_fields = ['title', 'course__title']

    try:
        admin.site.unregister(MaritimeEnrollment)
    except Exception:
        pass

    @admin.register(MaritimeEnrollment)
    class MaritimeEnrollmentAdmin(admin.ModelAdmin):
        list_display = ['user', 'course', 'status', 'enrolled_at']
        list_filter = ['status', 'enrolled_at']
        search_fields = ['user__username', 'course__title']

except ImportError:
    pass
except Exception:
    pass

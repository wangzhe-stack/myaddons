odoo.define('inventory_apply.InventoryKanban', function (require) {
"use strict";

var KanbanModel = require("web.KanbanModel");
var KanbanController = require("web.KanbanController");
var KanbanRenderer = require("web.KanbanRenderer");
var KanbanView = require("web.KanbanView");
var KanbanRecord = require("web.KanbanRecord");
var utils = require('web.utils');
var core = require('web.core');
var viewRegistry = require('web.view_registry');

var _t = core._t;
var qweb = core.qweb;
var DocumentViewer = require('inventory.selectDataPreView');


var InventoryKanbanController = KanbanController.extend({
    events: {
        'click #add_cart': '_onAddCart',
        'click .o_list_selection_box': '_onSelectDataPreView',
    },

    init: function(parent, model, renderer, params) {
        this._super.apply(this, arguments);
        this.recordSet = new Set();
    },

    _onAddCart: function(ev) {
        var self = this;
        var str = $(ev.target)[0]["dataset"]["id"];
//        var $button = $(ev.target);
//        $button.attr("disabled", true);
        var id = parseInt(str.replaceAll(',', ''));
        this.recordSet.add(id);
        this._renderSelectionBox();
    },

    _onSelectDataPreView: function (ev) {
        var self = this;
        var id_list = [];
        this.recordSet.forEach(function(element) {
            id_list.push(element)
        });
        this._rpc({
            model: 'inventory',
            method: 'get_inventory_data',
            args: ["", id_list],
        }).then(function (data) {
            var attachmentViewer = new DocumentViewer(self, data)
            attachmentViewer.appendTo($('body'));

        });
    },

    renderButtons: function ($node) {
        this._super.apply(this, arguments);
        this._renderSelectionBox();
    },

    _renderSelectionBox() {
        if (this.$selectionBox) {
            this.$selectionBox.remove();
            this.$selectionBox = null;
        }
        this.$selectionBox = $(qweb.render('Inventory.selection', {
            nbSelected: this.recordSet.size,
        }));
        this.$selectionBox.appendTo(this.$buttons);
    },
});

var InventoryKanbanView = KanbanView.extend({
    config: _.extend({}, KanbanView.prototype.config, {
        Model: KanbanModel,
        Controller: InventoryKanbanController,
        Renderer: KanbanRenderer,
    }),
});

viewRegistry.add('inventory_kanban_view', InventoryKanbanView);
});

odoo.define('inventory.selectDataPreView', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var QWeb = core.qweb;

    return Widget.extend({
        template: "selectDataPreView",
        events: {
            'click .o_close_btn': '_onClose',
            "click .fa-trash-o": '_onRemove',
            "click #cart_empty": '_clearCart',
            "click #cart_confirmed": '_genApply',
        },
        /**
         * The documentViewer takes an array of objects describing attachments in
         * argument, and the ID of an active attachment (the one to display first).
         * Documents that are not of type image or video are filtered out.
         */
        init: function (parent, retData) {
            this._super.apply(this, arguments);
            this.retData = retData;
        },

        /**
         * Open a modal displaying the active attachment
         * @override
         */
        start: function () {
            this.$el.modal('show');
//            this.$el.on('hidden.bs.modal', _.bind(this._onDestroy, this));
            return this._super.apply(this, arguments);
        },
        /**
         * @override
         */
        destroy: function () {
            if (this.isDestroyed()) {
                return;
            }
            this.$el.modal('hide');
            this.$el.remove();
            this._super.apply(this, arguments);
        },

        //--------------------------------------------------------------------------
        // Private
        //---------------------------------------------------------------------------

        /**
         * @private
         */
        _reset: function () {
            this.scale = 1;
            this.dragStartX = this.dragstopX = 0;
            this.dragStartY = this.dragstopY = 0;
        },
        /**
         * Render the active widget
         *
         * @private
         */
        _updateContent: function () {
            this.$('.o_viewer_content').html(QWeb.render('selectDataPreView.Content', {
                widget: this
            }));
            this._reset();
        },
        /**
         * Get CSS transform property based on scale and angle
         *
         * @private
         * @param {float} scale
         * @param {float} angle
         */
        // _getTransform: function (scale, angle) {
        //     return 'scale3d(' + scale + ', ' + scale + ', 1) rotate(' + angle + 'deg)';
        // },


        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent} e
         */
        _onClose: function (e) {
            e.preventDefault();
            this.destroy();
        },
        /**
         * When popup close complete destroyed modal even DOM footprint too
         *
         * @private
         */
        _onDestroy: function () {
            this.destroy();
        },

        _onRemove: function(ev) {
            ev.preventDefault();
            var $tr = $(ev.target).parent().parent();
            var tr_index = parseInt($tr[0].firstElementChild.innerText) - 1;
            this.retData.splice(tr_index, 1);
            var data_id = parseInt($tr[0].dataset.id);
            this._updateContent();
            this._updateSelectBox(data_id);
        },

        _updateSelectBox: function(data_id) {
            var parent = this.getParent();
            var $el = this.$el;
            parent.recordSet.delete(data_id);
            var $select_box = ($(parent.$el[0]).find(".o_list_selection_box"));
            $select_box[0].innerHTML = "<i class='fa fa-shopping-cart'/>&nbsp;&nbsp;"+ $el.find('tbody tr').length +" 已选取";
        },

        _clearCart: function() {
            this.retData.splice(0);
            this._updateContent();
            this._updateSelectBox();
            this.destroy();
        },

        _genApply: function() {
            var self = this;
            var $quantity = this.$el.find('.cart-plus-minus-box');
            var num_list = [];
            for(var i=0;i<$quantity.length;i++) {
                var quantity = $quantity[i].value
                num_list.push(quantity);
            }
            if(num_list.length === this.retData.length) {
                this.retData.forEach(function(element, index) {
                    element['number'] = parseInt(num_list[index]);
                });
            }
            this._rpc({
                model: 'inventory.apply',
                method: 'gen_inventory_apply',
                args: ["", this.retData],
            }).then(function(data) {
                self.do_action({
                    res_model: 'inventory.apply',
                    views: [[false, 'form']],
                    target: 'current',
                    type: 'ir.actions.act_window',
                    res_id: data,
                    context: {
                        'form_view_initial_mode': 'edit',
                    }
                });
                self._clearCart();
            })
        },

    });
});

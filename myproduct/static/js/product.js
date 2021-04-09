odoo.define('myproduct.report_product', function(require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Data = require("web.data");

    var Report_Product = AbstractAction.extend({
        template: "report.product",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;
            this._rpc({
                model: 'demo.product',
                method: 'get_data',
                args: [],
            }).then(function(data) {
                self.renderGrid(data);
            });
        },
        renderGrid: function(data) {
            var self = this;
            var source = {
                localdata: data,
                datatype: 'array',
                datafields:
                [
                    { name: 'first_name', type: 'string' },
                    { name: 'last_name', type: 'string' },
                    { name: 'product', type: 'string' },
                    { name: 'available', type: 'bool' },
                    { name: 'ship_date', type: 'date' },
                    { name: 'quantity', type: 'number' },
                    { name: 'price', type: 'number' }
                ]
            }
            var dataAdapter = new $.jqx.dataAdapter(source);
            $("#grid").jqxGrid(
            {
                width: "100%",
                autoheight: true,
                source: dataAdapter,
                theme: 'web',
                pageable: true,
                altrows: true,
                sortable: false,
                filterable: false,
                showfilterrow: false,
                altstart: 2,
                autoheight: true,
                autorowheight: true,
                selectionmode: 'multiplecellsextended',
                columnsresize: true,
                columnsautoresize: true,
                columns: [
                  { text: 'First Name', datafield: 'first_name', align: 'center', width: 130 },
                  { text: 'Last Name', datafield: 'last_name', align: 'center', width: 130 },
                  { text: 'ProductProduct ProductProductProductProductProductProductProductProduct', datafield: 'product', align: 'center', filtertype: 'checkedlist',
                    rendered: function (columnHeaderElement) {
//                      console.log(columnHeaderElement);
//                      console.log(columnHeaderElement.css('text-overflow'));
                      columnHeaderElement.css('text-overflow', 'initial');
//                      columnHeaderElement.css('word-break', 'break-word');
//                      columnHeaderElement.css('white-space', 'break-spaces');
//                      console.log(columnHeaderElement.css('text-overflow'));
                    },
                    autoheight: true,
                   },
                  { text: 'Available', datafield: 'available', columntype: 'checkbox', width: 67, cellsalign: 'center', align: 'center' },
                  { text: 'Ship Date', datafield: 'ship_date', width: 120, align: 'center', cellsalign: 'right', cellsformat: 'd' },
                  { text: 'Quantity', datafield: 'quantity', width: 70, align: 'center', cellsalign: 'right' },
                  { text: 'Price', datafield: 'price', cellsalign: 'right', align: 'center', cellsformat: 'c2' }
                ]
            });
        }
    });
    core.action_registry.add('action_report_product', Report_Product);
});
odoo.define('report_test.report_income', function(require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Data = require("web.data");

    var Report_Income = AbstractAction.extend({
        template: "report_income",
        init: function(parent, action) {
            this._super(parent, action);
        },
        start: function() {
            console.log("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            var self = this;
            this._rpc({
                model: 'jqx.income.report',
                method: 'get_data',
//                args: [],
            }).then(function(data) {
                console.log(data);
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
                    { name: 'id', type: 'number' },
                    { name: 'ccode', type: 'string' },
                    { name: 'cname', type: 'string' },
                    { name: 'je', type: 'number' }
                ]
            }
            var dataAdapter = new $.jqx.dataAdapter(source);
            $("#grid").jqxGrid(
            {
                width: "90%",
                autoheight: true,
                source: dataAdapter,
                theme: 'web',
                pageable: false,
                altrows: true,
                sortable: true,
                filterable: true,
                showfilterrow: true,
                altstart: 2,
                autoheight: true,
                autorowheight: true,
                selectionmode: 'multiplecellsextended',
                columnsresize: true,
                columnsautoresize: true,
                columns: [
                  { text: 'ID', datafield: 'id', align: 'center' },
                  { text: 'CCODE', columngroup: 'xxx', datafield: 'ccode', align: 'center' },
                  { text: 'CNAME', columngroup: 'xxx', datafield: 'cname', width: 200, align: 'center' },
                  { text: 'JE', columngroup: 'xxx', datafield: 'je', align: 'center', cellsalign: 'right', cellsformat: 'c4' }
                ],
                columngroups: [
                    { text: 'xxx', align: 'center', name: 'xxx' }
                ]
            });
        }
    });
    core.action_registry.add('action_report_income', Report_Income);
});
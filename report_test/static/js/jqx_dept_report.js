odoo.define('report_test.report_dept', function(require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Data = require("web.data");

    var Report_Dept = AbstractAction.extend({
        template: "report_dept",
        events: {'click #search': _.debounce(function () {
            var self = this;
            var year = $("#year").val();
            var sys = $("#share_kind_code").val();
            this._rpc({
                    model: 'jqx.dept.report',
                    method: 'get_data',
                    args: [ year, sys],
                }).then(function(data) {
                    self.renderGrid(data);
                });
        }, 200, true),},

        init: function(parent, action) {
            this._super(parent, action);
        },

        start: function() {
            var self = this;
            this._rpc({
                model: 'jqx.dept.report',
                method: 'get_data',
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
                    { name: 'c_dept_code', type: 'string' },
                    { name: 'c_dept_name', type: 'string' },
                    { name: 'i_money', type: 'number' },
                    { name: 'i_all_money', type: 'number' }
                ]
            }
            var dataAdapter = new $.jqx.dataAdapter(source);
            $("#grid").jqxGrid(
            {
                width: "90%",
                source: dataAdapter,
                theme: 'energyblue',
                pageable: false,
                altrows: true,
                sortable: true,
                filterable: true,
                showfilterrow: true,
                altstart: 1,
                autoheight: false,
                autorowheight: false,
                columns: [
                  { text: 'CDEPTCODE', datafield: 'c_dept_code', align: 'center' },
                  { text: 'CDEPTNAME', datafield: 'c_dept_name', align: 'center' },
                  { text: 'IMONEY', datafield: 'i_money', width: 200, align: 'center', cellsformat: 'c4' },
                  { text: 'IALLMONEY', datafield: 'i_all_money', align: 'center', cellsalign: 'right',
                    cellsformat: 'c4' }
                ],
            });
        }
    });
    core.action_registry.add('action_report_dept', Report_Dept);
});
odoo.define('myproduct.report_member', function(require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Data = require("web.data");

    var Report_Member = AbstractAction.extend({
        template: "report.member",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;
            this._rpc({
                model: 'member',
                method: 'get_data',
                args: [],
            }).then(function(data) {
                self.renderGrid(data);
            });
        },
        renderGrid: function(data) {
            var self = this;
            var source = {
                localData: data,
                dataType: 'json',
                dataFields: [
                    { name: 'employee_key', type: 'number' },
                    { name: 'parent_employee_key', type: 'number' },
                    { name: 'first_name', type: 'string' },
                    { name: 'last_name', type: 'string' },
                    { name: 'title', type: 'string' },
                    { name: 'hire_date', type: 'date' },
                    { name: 'birth_date', type: 'date' }
                ],
                hierarchy:
                {
                    keyDataField: { name: 'employee_key' },
                    parentDataField: { name: 'parent_employee_key' }
                },
                id: 'employee_key',
            };
            var dataAdapter = new $.jqx.dataAdapter(source);
            $("#treegrid").jqxTreeGrid(
            {
                width: "90%",
                source: dataAdapter,
                sortable: true,
                theme: 'dark',
                ready: function()
                {
                    $("#treegrid").jqxTreeGrid('expandRow', '2');
                },
                columns: [
                  { text: 'FirstName', columnGroup: 'Name', dataField: 'first_name', width: 200 },
                  { text: 'LastName', columnGroup: 'Name', dataField: 'last_name', width: 200 },
                  { text: 'Title', dataField: 'title', width: 160 },
                  { text: 'Birth Date', dataField: 'birth_date', cellsFormat: 'd', width: 120 },
                  { text: 'Hire Date', dataField: 'hire_date', cellsFormat: 'd' },
                ],
                columnGroups: [
                  { text: 'Name', name: 'Name' }
                ]
            });
        }
    });
    core.action_registry.add('action_report_member', Report_Member);
});
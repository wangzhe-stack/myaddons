odoo.define('geo.gis_search', function(require) {
    "use strict";

    var core = require("web.core");
    var AbstractAction = require("web.AbstractAction");
    var Data = require("web.data");

    var Gis_Search = AbstractAction.extend({
        template: "geo_gis_search",
        events: {
            "click #search": '_search_project_position',
            "click #clear": _.debounce(function () {
                var self = this;
                var code = $("#code").val('');
                var name = $("#name").val('');
            }, 200, true),
        },

        init: function(parent, action) {
            this._super(parent, action);
            var series = [{
                name: '项目详情',
                type: 'scatter',
                coordinateSystem: 'bmap',
                data: [],
                symbol: 'diamond',
                symbolSize: 10,
                label: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                itemStyle: {
                    color: '#2196f3'
                },
                emphasis: {
                    label: {
                        show: true
                    }
                }
            }];
            this.option = {
                title: {
                        text: '项目地理位置查询',
                        left: 'center'
                    },
                bmap: {
                    center: [108.946465,34.347269],
                    zoom: 7,
                    aspectScale: 0.75,
                    roam: true,
                    mapStyle: {
                        styleJson: [{
                            'featureType': 'water',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#d1d1d1'
                            }
                        }, {
                            'featureType': 'land',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#f3f3f3'
                            }
                        }, {
                            'featureType': 'railway',
                            'elementType': 'all',
                            'stylers': {
                                'visibility': 'off'
                            }
                        }, {
                            'featureType': 'highway',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#fdfdfd'
                            }
                        }, {
                            'featureType': 'highway',
                            'elementType': 'labels',
                            'stylers': {
                                'visibility': 'off'
                            }
                        }, {
                            'featureType': 'arterial',
                            'elementType': 'geometry',
                            'stylers': {
                                'color': '#fefefe'
                            }
                        }, {
                            'featureType': 'arterial',
                            'elementType': 'geometry.fill',
                            'stylers': {
                                'color': '#fefefe'
                            }
                        }, {
                            'featureType': 'poi',
                            'elementType': 'all',
                            'stylers': {
                                'visibility': 'off'
                            }
                        }, {
                            'featureType': 'green',
                            'elementType': 'all',
                            'stylers': {
                                'visibility': 'off'
                            }
                        }, {
                            'featureType': 'subway',
                            'elementType': 'all',
                            'stylers': {
                                'visibility': 'off'
                            }
                        }, {
                            'featureType': 'manmade',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#d1d1d1'
                            }
                        }, {
                            'featureType': 'local',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#d1d1d1'
                            }
                        }, {
                            'featureType': 'arterial',
                            'elementType': 'labels',
                            'stylers': {
                                'visibility': 'off'
                            }
                        }, {
                            'featureType': 'boundary',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#fefefe'
                            }
                        }, {
                            'featureType': 'building',
                            'elementType': 'all',
                            'stylers': {
                                'color': '#d1d1d1'
                            }
                        }, {
                            'featureType': 'label',
                            'elementType': 'labels.text.fill',
                            'stylers': {
                                'color': '#999999'
                            }
                        }]
                    }
                },
                tooltip : {
                    trigger: 'item',
                    formatter: function(params) {
                        var res = "项目名称:" + params.name + "<br/>";
                        var myseries = series;
                        for(var j=0;j<myseries[0].data.length;j++){
                            if(myseries[0].data[j].name==params.name){
                                res += "承担单位:" + myseries[0].data[j].value[4] + "<br/>" +
                                       "所在地区:" + myseries[0].data[j].value[3];
                            }
                        }
                        return res;
                    },
                },
                series : series,
            };
        },
        convertData: function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                res.push({
                    name: data[i].name,
                    value: data[i]['position'].concat([data[i]['area'],data[i]['assume_unit']])
                });
            }
            return res;
        },
        render_map: function() {
            var self = this;
            $(document).ready(function() {
                var myChart = echarts.init(document.getElementById('allmap'));
                myChart.setOption(self.option);
            });
        },

        start: function() {
            this.render_map();
        },

        _search_project_position: function() {
            var self = this;
            var code = $("#code").val();
            var name = $("#name").val();
            if(code || name) {
                this._rpc({
                    model: 'geo.project',
                    method: 'search_position',
                    args: ["", code, name],
                }).then(function (result) {
                    var data = self.convertData(result);
                    self.option.series[0]['data'] = data;
                    self.render_map();
                });
            }
        },

    });
    core.action_registry.add('action_gis_search', Gis_Search);
});
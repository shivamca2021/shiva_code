odoo.define('prism.dashboard', function (require) {
'use strict';

var AbstractAction = require('web.AbstractAction');
var ajax = require('web.ajax');
var core = require('web.core');
var Dialog = require('web.Dialog');
var field_utils = require('web.field_utils');
var pyUtils = require('web.py_utils');
var session = require('web.session');
var time = require('web.time');
var web_client = require('web.web_client');

var _t = core._t;
var QWeb = core.qweb;



var Dashboard = AbstractAction.extend({
    hasControlPanel: true,
    contentTemplate: 'prismDashboardMain',
    jsLibs: [
        '/prism_dashboard/static/lib/js/Chart.min.js',
    ],
    
    init: function(parent, context) {
        this._super(parent, context);
		this.dataset_db = [];
    },

   /*start: function() {
        var self = this;
        return this._super().then(function() {
		    var prom =  self._rpc({
		        model: 'dashboard.report',
		        method: 'get_differdays_dashboard',
		        args: [[]],
		        })
		      	prom.then(function (results) {
		      		var array_datasets = [];
		            $.each(results, function( index, value ) {
	            		  var r = Math.floor(Math.random() * 255);
				          var g = Math.floor(Math.random() * 255);
				          var b = Math.floor(Math.random() * 255);
				          var color =  "rgb(" + r + "," + g + "," + b + ")";
						  array_datasets.push({
								label: "Hourly dataset "+index,
								fillColor : "transparent",
								strokeColor : color,
								pointColor : color,
								backgroundColor: "#fff",
								pointStrokeColor : "#fff", 
								pointHighlightFill : "#fff",
								pointHighlightStroke : "rgba(151,187,205,1)",
								hoverBorderColor: '#71B37C',
								data : results[index]
							})
					});
					var lineChartData = {
						labels : ["Opportunity","Sale Order","Purchase Order","Manufacturing","Work Order","Delivery Order"],
						datasets : array_datasets
			
					};
					
					self.$("#canvas").each(function(index, element) {
					    var context = element.getContext('2d');
					    var options = {
				                responsive: true,
				                legend: {
						                position: 'top',
						                display: true
							            },
					            title: {
					                display: true,
					                text: 'Chart'
					            }         
				            }
					    self.myLine = new Chart(context).Line(lineChartData, options);
					});
		        });
		        
        });
    },*/
	start: function() {
		var self = this;
        return this._super().then(function() {
        	var prom =  self._rpc({
		        model: 'dashboard.report',
		        method: 'get_differdays_dashboard',
		        args: [[]],
		        });
	        prom.then(function (results) {
	        	var array_datasets = [];
	            $.each(results, function( index, value ) {
            		  var r = Math.floor(Math.random() * 255);
			          var g = Math.floor(Math.random() * 255);
			          var b = Math.floor(Math.random() * 255);
			          var color =  "rgb(" + r + "," + g + "," + b + ")";
					  array_datasets.push({
								label: results[index][0],
								backgroundColor: color,
								borderColor:color,
								data: results[index][1],
								fill: false,
						})
				});
	        	self.$("#canvas").each(function(index, element) {
				    var context = element.getContext('2d');
				    
					var labels = ["Opp to Qoute", "Sale Order","Manufacturing Order Start","Purchase Order","Shipment Received","Work Order Start","Work Order End","Manufacturing Order End","Delivery Order","Installation Date"];
					var config = {
					  type: 'line',
					  data: {
					    labels: labels,
					    datasets: array_datasets
					  },
					  options: {
					    responsive: true,
					    legend: {
				                display: true
						   },
					    plugins: {
				            legend: {
				                display: true
						   }
				        },
					    title:{
					      display:false,
					      text:'Chart.js Line Chart'
					    },
					    interaction: {
				            mode: 'x'
				        },
					    tooltips: {
					      mode: 'nearest',
					      intersect: true
					    },
					   hover: {
					      mode: 'nearest',
					      intersect: true
					    },
					    scales: {
					      xAxes: [{
					        display: true,
					        scaleLabel: {
					          display: false,
					          labelString: 'Month'
					        },
					        ticks: {
								autoSkip: false
								}
					      }],
					      yAxes: [{
					        display: true,
					        scaleLabel: {
					          display: true,
					        },
					      }]
					    }
					  }
					};
					self.myLine = new Chart(context, config);
				    
				});
			});
        });
	},
   
});

core.action_registry.add('prism_chart_dashboard', Dashboard);

return Dashboard;
});

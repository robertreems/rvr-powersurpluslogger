
@description('Generated from /subscriptions/1cf68e52-3db2-4412-9a55-54a79c2aaccf/resourceGroups/dashboards/providers/Microsoft.Portal/dashboards/7d2ae596-be5a-4b4c-954a-0d7d528f6146')
resource daebeabcaddf 'Microsoft.Portal/dashboards@2020-09-01-preview' = {
  properties: {
    lenses: [
      {
        order: 0
        parts: [

          {
            position: {
              x: 0
              y: 0
              rowSpan: 6
              colSpan: 4
            }
            metadata: {
              inputs: [
                {
                  name: 'resourceTypeMode'
                  isOptional: true
                }
                {
                  name: 'ComponentId'
                  isOptional: true
                }
                {
                  name: 'Scope'
                  value: {
                    resourceIds: [
                      '/subscriptions/1cf68e52-3db2-4412-9a55-54a79c2aaccf/resourcegroups/rvrlogging/providers/microsoft.operationalinsights/workspaces/myfirstloganalytics'
                    ]
                  }
                  isOptional: true
                }
                {
                  name: 'PartId'
                  value: '08809335-4861-4d35-b2f7-d4c9f154df6e'
                  isOptional: true
                }
                {
                  name: 'Version'
                  value: '2.0'
                  isOptional: true
                }
                {
                  name: 'TimeRange'
                  isOptional: true
                }
                {
                  name: 'DashboardId'
                  isOptional: true
                }
                {
                  name: 'DraftRequestParameters'
                  isOptional: true
                }
                {
                  name: 'Query'
                  value: 'power_usage_CL \n| where metric_name_s == "aggregated_power"\n| where  TimeGenerated > startofday(now())\n'
                  isOptional: true
                }
                {
                  name: 'ControlType'
                  value: 'FrameControlChart'
                  isOptional: true
                }
                {
                  name: 'SpecificChart'
                  value: 'Line'
                  isOptional: true
                }
                {
                  name: 'PartTitle'
                  value: 'Analytics'
                  isOptional: true
                }
                {
                  name: 'PartSubTitle'
                  value: 'myfirstloganalytics'
                  isOptional: true
                }
                {
                  name: 'Dimensions'
                  value: {
                    xAxis: {
                      name: 'TimeGenerated'
                      type: 'datetime'
                    }
                    yAxis: [
                      {
                        name: 'value_d'
                        type: 'real'
                      }
                    ]
                    splitBy: [
                      {
                        name: 'TenantId'
                        type: 'string'
                      }
                    ]
                    aggregation: 'Sum'
                  }
                  isOptional: true
                }
                {
                  name: 'LegendOptions'
                  value: {
                    isEnabled: true
                    position: 'Bottom'
                  }
                  isOptional: true
                }
                {
                  name: 'IsQueryContainTimeRange'
                  value: true
                  isOptional: true
                }
              ]
              type: 'Extension/Microsoft_OperationsManagementSuite_Workspace/PartType/LogsDashboardPart'
              settings: {
                content: {
                  Query: 'power_usage_CL \n| where metric_name_s == "aggregated_power"\n| where  TimeGenerated > startofday(now())\n| extend hour = TimeGenerated\n| extend kWh = value_d\n'
                  PartTitle: 'Power consumption & production'
                  PartSubTitle: 'Today'
                  Dimensions: {
                    xAxis: {
                      name: 'TimeGenerated'
                      type: 'datetime'
                    }
                    yAxis: [
                      {
                        name: 'kWh'
                        type: 'real'
                      }
                    ]
                    splitBy: [
                      {
                        name: 'TenantId'
                        type: 'string'
                      }
                    ]
                    aggregation: 'Sum'
                  }
                }
              }
            }
          }

          {
            position: {
              x: 0
              y: 6
              rowSpan: 6
              colSpan: 4
            }
            metadata: {
              inputs: [
                {
                  name: 'resourceTypeMode'
                  isOptional: true
                }
                {
                  name: 'ComponentId'
                  isOptional: true
                }
                {
                  name: 'Scope'
                  value: {
                    resourceIds: [
                      '/subscriptions/1cf68e52-3db2-4412-9a55-54a79c2aaccf/resourcegroups/rvrlogging/providers/microsoft.operationalinsights/workspaces/myfirstloganalytics'
                    ]
                  }
                  isOptional: true
                }
                {
                  name: 'PartId'
                  value: '77a1d94b-1da2-401c-88e3-1881866b62a3'
                  isOptional: true
                }
                {
                  name: 'Version'
                  value: '2.0'
                  isOptional: true
                }
                {
                  name: 'TimeRange'
                  value: 'P7D'
                  isOptional: true
                }
                {
                  name: 'DashboardId'
                  isOptional: true
                }
                {
                  name: 'DraftRequestParameters'
                  isOptional: true
                }
                {
                  name: 'Query'
                  value: 'let dataset = materialize(power_usage_CL);\n//\nlet myFunction = (T: (metric_name_s: string, TimeGenerated: datetime, value_d: real), arg0: string) {\n    let delivery_minValue = dataset\n        | where metric_name_s has strcat("delivery_", arg0)\n        | summarize min(value_d) by Day=bin(TimeGenerated, 1d), metric_name_s;\n    let consumption_minValue = dataset\n        | where metric_name_s has strcat("consumption_", arg0)\n        | summarize min(value_d) by Day=bin(TimeGenerated, 1d), metric_name_s;\n    let consumption_maxValue = dataset\n        | where metric_name_s has strcat("consumption_", arg0)\n        | summarize max(value_d) by Day=bin(TimeGenerated, 1d), metric_name_s;\n    //\n    T\n    | where metric_name_s contains strcat("delivery_", arg0)\n    | summarize max(value_d) by Day=bin(TimeGenerated, 1d), metric_name_s\n    | join delivery_minValue on Day\n    | extend sum_delivery = max_value_d - min_value_d\n    | join consumption_minValue on Day\n    | join consumption_maxValue on Day\n    | extend sum_consumption = max_value_d1 - min_value_d1\n    | extend total = sum_delivery - sum_consumption\n    | project Day, metric_name_s, total, sum_delivery, sum_consumption\n};\nunion \n    myFunction(dataset, "tariff1"),\n    myFunction(dataset, "tariff2")\n| sort by Day\n| render columnchart with (kind=stacked, ysplit=none, ytitle="kWh")\n'
                  isOptional: true
                }
                {
                  name: 'ControlType'
                  value: 'FrameControlChart'
                  isOptional: true
                }
                {
                  name: 'SpecificChart'
                  value: 'StackedColumn'
                  isOptional: true
                }
                {
                  name: 'PartTitle'
                  value: 'Power consumption & production'
                  isOptional: true
                }
                {
                  name: 'PartSubTitle'
                  value: 'Daily'
                  isOptional: true
                }
                {
                  name: 'Dimensions'
                  value: {
                    xAxis: {
                      name: 'Day'
                      type: 'datetime'
                    }
                    yAxis: [
                      {
                        name: 'total'
                        type: 'real'
                      }
                    ]
                    splitBy: [
                      {
                        name: 'metric_name_s'
                        type: 'string'
                      }
                    ]
                    aggregation: 'Sum'
                  }
                  isOptional: true
                }
                {
                  name: 'LegendOptions'
                  value: {
                    isEnabled: true
                    position: 'Bottom'
                  }
                  isOptional: true
                }
                {
                  name: 'IsQueryContainTimeRange'
                  value: false
                  isOptional: true
                }
              ]
              type: 'Extension/Microsoft_OperationsManagementSuite_Workspace/PartType/LogsDashboardPart'
              settings: {}
            }
          }
          
          {
            position: {
              x: 0
              y: 12
              rowSpan: 6
              colSpan: 4
            }
            metadata: {
              inputs: [
                {
                  name: 'resourceTypeMode'
                  isOptional: true
                }
                {
                  name: 'ComponentId'
                  isOptional: true
                }
                {
                  name: 'Scope'
                  value: {
                    resourceIds: [
                      '/subscriptions/1cf68e52-3db2-4412-9a55-54a79c2aaccf/resourcegroups/rvrlogging/providers/microsoft.operationalinsights/workspaces/myfirstloganalytics'
                    ]
                  }
                  isOptional: true
                }
                {
                  name: 'PartId'
                  value: '7879c43d-1ae6-462a-b939-f0ade360cd2e'
                  isOptional: true
                }
                {
                  name: 'Version'
                  value: '2.0'
                  isOptional: true
                }
                {
                  name: 'TimeRange'
                  value: '2022-05-14T20:34:59.000Z/2022-05-28T20:34:59.736Z'
                  isOptional: true
                }
                {
                  name: 'DashboardId'
                  isOptional: true
                }
                {
                  name: 'DraftRequestParameters'
                  isOptional: true
                }
                {
                  name: 'Query'
                  value: 'let dataset = materialize(power_usage_CL);\n//\nlet myFunction = (T: (metric_name_s: string, TimeGenerated: datetime, value_d: real), arg0: string) {\n    let delivery_minValue = dataset\n        | where metric_name_s has strcat("delivery_", arg0)\n        | summarize min(value_d) by Day=bin(TimeGenerated, 7d), metric_name_s;\n    let consumption_minValue = dataset\n        | where metric_name_s has strcat("consumption_", arg0)\n        | summarize min(value_d) by Day=bin(TimeGenerated, 7d), metric_name_s;\n    let consumption_maxValue = dataset\n        | where metric_name_s has strcat("consumption_", arg0)\n        | summarize max(value_d) by Day=bin(TimeGenerated, 7d), metric_name_s;\n    //\n    T\n    | where metric_name_s contains strcat("delivery_", arg0)\n    | summarize max(value_d) by Day=bin(TimeGenerated, 7d), metric_name_s\n    | join delivery_minValue on Day\n    | extend sum_delivery = max_value_d - min_value_d\n    | join consumption_minValue on Day\n    | join consumption_maxValue on Day\n    | extend sum_consumption = max_value_d1 - min_value_d1\n    | extend total = sum_delivery - sum_consumption\n    | project Day, metric_name_s, total, sum_delivery, sum_consumption\n};\nunion \n    myFunction(dataset, "tariff1"),\n    myFunction(dataset, "tariff2")\n| sort by Day\n| render columnchart with (kind=stacked, ysplit=none, ytitle="kWh")\n'
                  isOptional: true
                }
                {
                  name: 'ControlType'
                  value: 'FrameControlChart'
                  isOptional: true
                }
                {
                  name: 'SpecificChart'
                  value: 'StackedColumn'
                  isOptional: true
                }
                {
                  name: 'PartTitle'
                  value: 'Power consumption & production'
                  isOptional: true
                }
                {
                  name: 'PartSubTitle'
                  value: 'Weekly'
                  isOptional: true
                }
                {
                  name: 'Dimensions'
                  value: {
                    xAxis: {
                      name: 'Day'
                      type: 'datetime'
                    }
                    yAxis: [
                      {
                        name: 'total'
                        type: 'real'
                      }
                    ]
                    splitBy: [
                      {
                        name: 'metric_name_s'
                        type: 'string'
                      }
                    ]
                    aggregation: 'Sum'
                  }
                  isOptional: true
                }
                {
                  name: 'LegendOptions'
                  value: {
                    isEnabled: true
                    position: 'Bottom'
                  }
                  isOptional: true
                }
                {
                  name: 'IsQueryContainTimeRange'
                  value: false
                  isOptional: true
                }
              ]
              type: 'Extension/Microsoft_OperationsManagementSuite_Workspace/PartType/LogsDashboardPart'
              settings: {}
            }
          }
        ]
      }
    ]
    metadata: {
      model: {
        timeRange: {
          value: {
            relative: {
              duration: 24
              timeUnit: 1
            }
          }
          type: 'MsPortalFx.Composition.Configuration.ValueTypes.TimeRange'
        }
        filterLocale: {
          value: 'en-us'
        }
        filters: {
          value: {
            MsPortalFx_TimeRange: {
              model: {
                format: 'local'
                granularity: 'auto'
                relative: '7d'
              }
              displayCache: {
                name: 'UTC Time'
                value: 'Past 7 days'
              }
              filteredPartIds: [
                'StartboardPart-LogsDashboardPart-ced3d8ac-90b1-4375-b7e0-acecfbd76068'
                'StartboardPart-LogsDashboardPart-ced3d8ac-90b1-4375-b7e0-acecfbd7609b'
              ]
            }
          }
        }
      }
    }
  }
  location: 'westeurope'
  tags: {
    'hidden-title': 'Power consumption & production mobile'
  }
  name: '7d2ae596-be5a-4b4c-954a-0d7d528f6146'
}

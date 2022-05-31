
@description('Generated from /subscriptions/1cf68e52-3db2-4412-9a55-54a79c2aaccf/resourceGroups/dashboards/providers/Microsoft.Portal/dashboards/5d3272de-8230-46e6-b3d5-47a790a10057')
resource ddeebdaa 'Microsoft.Portal/dashboards@2020-09-01-preview' = {
  properties: {
    lenses: [
      {
        order: 0
        parts: [
          {
            position: {
              x: 0
              y: 0
              rowSpan: 8
              colSpan: 16
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
                  value: '9b798da1-40ab-407f-a714-ca83f209abe7'
                  isOptional: true
                }
                {
                  name: 'Version'
                  value: '2.0'
                  isOptional: true
                }
                {
                  name: 'TimeRange'
                  value: 'P1D'
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
                  value: 'app_event_CL  | where type_s  contains "error" or type_s contains "warning"\n'
                  isOptional: true
                }
                {
                  name: 'ControlType'
                  value: 'AnalyticsGrid'
                  isOptional: true
                }
                {
                  name: 'SpecificChart'
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
                  isOptional: true
                }
                {
                  name: 'LegendOptions'
                  isOptional: true
                }
                {
                  name: 'IsQueryContainTimeRange'
                  value: false
                  isOptional: true
                }
              ]
              type: 'Extension/Microsoft_OperationsManagementSuite_Workspace/PartType/LogsDashboardPart'
              settings: {
                content: {
                  GridColumnsWidth: {
                    Message: '1116px'
                  }
                  Query: 'app_event_CL  | where type_s  contains "error" or type_s contains "warning" | project TimeGenerated, Message\n\n'
                }
              }
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
                format: 'utc'
                granularity: 'auto'
                relative: '24h'
              }
              displayCache: {
                name: 'UTC Time'
                value: 'Past 24 hours'
              }
              filteredPartIds: [
                'StartboardPart-LogsDashboardPart-5b1159af-52e0-4237-afea-8524a9d15198'
              ]
            }
          }
        }
      }
    }
  }
  location: 'westeurope'
  tags: {
    'hidden-title': 'App errors and warnings'
  }
  name: 'App_Warning_Errors'
}

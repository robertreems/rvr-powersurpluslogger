
@description('Generated from /subscriptions/1cf68e52-3db2-4412-9a55-54a79c2aaccf/resourceGroups/rvrlogging/providers/Microsoft.OperationalInsights/workspaces/MyfirstLogAnalytics')
resource MyfirstLogAnalytics 'Microsoft.OperationalInsights/workspaces@2021-12-01-preview' = {
  properties: {
    source: 'Azure'
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 730
    features: {
      legacy: 0
      searchVersion: 1
      enableLogAccessUsingOnlyResourcePermissions: true
    }
    workspaceCapping: {
      dailyQuotaGb: '-1.0'
    }
    publicNetworkAccessForIngestion: 'Enabled'
    publicNetworkAccessForQuery: 'Enabled'
  }
  name: 'MyfirstLogAnalytics'
  location: 'westeurope'
  tags: {}
}

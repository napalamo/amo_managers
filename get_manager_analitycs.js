let data = request.array

let statuses = table.find("pipeline_statuses", ["id", "status_id", "name"], [["id", ">", 5]])
let managers = table.find("managers", ["manager_id", "manager_name"], [
  ["is_deleted", "=", "0"]
])

let countLeadsToManagers = []

for (let manager of managers) {
  let managerData = {
    manager_id: manager.manager_id,
    manager_name: manager.manager_name,
    statuses: []
  }

  for (let status of statuses) {
    let leadsCountToStatus = table.count("unsorted_log", [
      ["created_at", ">", data.start_date],
      ["created_at", "<", data.end_date],
      ["manager_id", "=", manager.manager_id],
      ["status_id", "=", status.status_id],
      ["type_lead", "=", data.type_lead]      
    ])

    managerData.statuses.push({
      id: status.id,
      status_id: status.status_id,
      name: status.name,
      lead_count: leadsCountToStatus
    })
  }

  countLeadsToManagers.push(managerData)
}

return countLeadsToManagers

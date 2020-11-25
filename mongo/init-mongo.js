db.createUser({
    user: 'telerik',
    pwd: '123',
    roles: [
      {
        role: 'readWrite',
        db: 'coronaz'
      }
    ]
  })

db.createUser({
    user: 'telerik',
    pwd: '123',
    roles: [
      {
        role: 'readWrite',
        db: 'numtest'
      }
    ]
  })
  
db.numtest.insert({"msg":"initDatabase"})
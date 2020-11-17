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
  
db.coronaz.insert({"msg":"initDatabase"})

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
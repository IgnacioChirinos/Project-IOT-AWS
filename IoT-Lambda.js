console.log('Loading function');
const AWS = require('aws-sdk');
const dynamo = new AWS.DynamoDB.DocumentClient();
const collection = 'IoTCatalog';
// Handler lamda function
exports.handler = function (event, context) {
  console.log('Received event:', JSON.stringify(event, null, 2));
  const params = {
    TableName: collection,
    Item: {
      serialNumber: event.Id,
      timeStamp: event.timestamp,
      Temperatura: event.temperature,
      Humedad: event.humidity,
    },
  };
  console.log('Saving Telemetry Data');
  dynamo.put(params, function (err, data) {
    if (err) {
      console.error(
        'Unable to add device. Error JSON:',
        JSON.stringify(err, null, 2)
      );
      context.fail();
    } else {
      console.log(data);
      console.log('Data saved:', JSON.stringify(params, null, 2));
      context.succeed();
      return { message: 'Item created in DB' };
    }
  });
};

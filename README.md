# CognitiveServiceTokenAuth

## Benefits

+ Avoid exposing the access keys of Azure Cognitive Services to improve security
+ Support a large number of clients to connect to Azure Cognitive Services at high frequency

## Scenarios

This method is suitable for B2C scenarios: a large number of clients need to link to Azure Cognitive Services, and for security reasons, the key of Cognitive Services cannot be delivered to the device for direct use.

Specific applicable scenarios such as:
+ Use Cognitive Services' speech translation feature on the mobile app
+ Use the text-to-speech and speech-to-text functions of Cognitive Services on mobile phones, desktop apps, or web pages

## Why access token?

The specific difference between the access token Token and the key is that **the access token is dynamic** and is updated every ten minutes. The client needs to verify the legitimacy of the client only when it initiates a connection with Cognitive Services. At this point, the token can be used to implement client legitimacy verification, and once the verification is passed, the access token is no longer needed. Cognitive Services will not verify the legitimacy of the client in subsequent communications until the end of this connection.

Access keys are relatively fixed. Unless an administrator actively updates it, the access key remains the same. Once the key is leaked on the client side, unauthorized users will have the opportunity to use the paid subscription of legitimate users to use Azure Cognitive Services. This poses a security risk to scenarios with a large number of clients.

## Obtain access token

The access token needs to be obtained by accessing the IssueToken function of the service endpoint in the form of an HTTP request.

```python
def retrieve_token(app, endpoint, key):
    with app.app_context():
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': key,
            'Content-length': '0'
        }
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 200:
            global token
            token = response.text
            return jsonify({'token': token})
        else:
            return None
```
Since the access token changes dynamically every ten minutes, the service that caches the access token information needs to periodically refresh the access token at an interval of less than 10 minutes, so as to ensure that the client can obtain a valid access token every time it requests card data.

To obtain an access token, a Cognitive Services key is required. In order to ensure that the key is always placed on the server rather than the client, it is necessary to build a REST API service. On the one hand, the service uses the key stored on the server to obtain and cache the access token, and on the other hand, it responds to a large number of clients' applications for the access token.

In the src/python/app.py file, a simple REST API service is built using the flask framework. Access the /token/ path of the service to obtain the access token directly. In a production environment, this REST API needs to be protected by the system's authentication to prevent unauthorized clients from obtaining access tokens.

This REST API service starts a background thread that periodically accesses Azure Cognitive Services to refresh the access token data.

To start this REST API service, please set COGNITIVE_SERVICE_ENDPOINT and COGNITIVE_SERVICE_KEY environment variables. The value you could find from Azure portal of Cognitive Service resource.

## Connect to Azure Cognitive Services using an access token

Accessing Azure Cognitive Services using an access token is simple. For Azure Speech SDK Python, you need to specify the auth_token parameter when constructing the SpeechConfig object:

```python
speech_config = speechsdk.SpeechConfig(auth_token=token, region=region)
```

The complete test code can be found in the src/testClient/test.py file.

For Azure Speech SDK JavaScript, the SpeechConfig object needs to be constructed using the [fromAuthenticationToken()](https://learn.microsoft.com/en-us/javascript/api/microsoft-cognitiveservices-speech-sdk/speechconfig?view=azure-node-latest#microsoft-cognitiveservices-speech-sdk-speechconfig-fromauthorizationtoken) method.

## Reference:
[Authenticate with an access token](https://learn.microsoft.com/en-us/azure/cognitive-services/authentication?tabs=powershell#authenticate-with-an-access-token)

# 使用令牌访问Azure 认知服务

## 作用
+ 避免暴露Azure 认知服务的访问密钥，提升安全性
+ 支持大量的客户端高频率连接Azure 认知服务

## 适用场景
该方法适用于B2C 的场景：大量客户端需要链接Azure 认知服务，且处于安全考虑不能将认知服务的密钥下发到设备上直接使用。

具体的适用场景如：
+ 在手机app 上使用认知服务的语音翻译功能
+ 在手机或者桌面App又或者是Web 页面上使用认知服务的文本转语音、语音转文本功能

## 为什么要使用令牌？
访问令牌Token 与密钥的具体区别是：**访问令牌是动态的**，每隔十分钟就更新一次。客户端只有在与认知服务发起连接时，需要验证客户端的合法性。此时令牌可以用来实现客户端合法性验证，一旦验证通过就不再需要访问令牌了。认知服务在后续的通讯中将不再验证客户端合法性直到本次连接结束。

访问密钥则是相对固定的。如果不是管理人员主动更新，那么访问密钥则一直保持不变。一旦密钥在客户端泄露，非法用户将有机会利用合法用户的付费订阅使用Azure 认知服务。这给具有大量客户端的场景带来了安全风险。

## 访问令牌的获取
访问令牌需要以HTTP请求的方式通过访问服务终结点的IssueToken 功能获得。
```python
def retrieve_token(app, endpoint, key):
    with app.app_context():
        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': key,
            'Content-length': '0'
        }
        response = requests.post(endpoint, headers=headers)
        if response.status_code == 200:
            global token
            token = response.text
            return jsonify({'token': token})
        else:
            return None
```
由于访问令牌每十分钟会动态变化，所以缓存访问令牌信息的服务需要以小于10分钟的间隔周期性地刷新访问令牌，以此确保客户端每次请求都能获取到有效的访问令牌数据。

获取访问令牌，需要使用认知服务密钥。为了保证密钥始终放置在服务端而不是客户端，因此有必要构建一个REST API 服务。该服务一方面利用保存在服务器上的密钥获取并缓存访问令牌，另一方面则响应大量客户端对访问令牌的申请。

在src/python/app.py 文件中，利用flask 框架构建了一个简单的REST API 服务。访问该服务的/token/路径直接可以获得访问令牌。 在生产环境中，**这个REST API 需要被系统的身份验证保护**，避免未授权客户端也可以获取访问令牌。

这个REST API 服务启动了一个后台线程，周期性地访问Azure 认知服务刷新访问令牌数据。

要启动此 REST API 服务，请设置 COGNITIVE_SERVICE_ENDPOINT 和 COGNITIVE_SERVICE_KEY 环境变量。 您可以从认知服务资源的 Azure 门户中找到的值。

## 使用访问令牌连接Azure 认知服务
使用访问令牌访问Azure 认知服务很简单。对于Azure Speech SDK Python 来说，需要在构建SpeechConfig对象的时候指定auth_token 参数：
```python
speech_config = speechsdk.SpeechConfig(auth_token=token, region=region)
```
完整的测试代码可以在src/testClient/test.py 文件中找到。

对于Azure Sppech SDK JavaScript 来说，需要使用[fromAuthenticationToken()](https://learn.microsoft.com/en-us/javascript/api/microsoft-cognitiveservices-speech-sdk/speechconfig?view=azure-node-latest#microsoft-cognitiveservices-speech-sdk-speechconfig-fromauthorizationtoken) 方法构建SpeechConfig 对象。

## 参考链接:
[使用访问令牌进行身份验证](https://learn.microsoft.com/zh-cn/azure/cognitive-services/authentication?tabs=powershell#authenticate-with-an-access-token)
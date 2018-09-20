# A note on Tinycoin execution using Docker Toolbox
Docker Toolbox is for non Windows 10 systems - https://docs.docker.com/

### 01. Install docker tool box on the Windows System. Docker toolbox by default has a Linux distribution with it.
 
### 02. Invoking the docker tool box, invokes a VM also.
   Please note down the IP address provided by docker tool box. It is 192.168.99.100 on the author's machine.
   
### 03. Change your working directory to the tinycoin directory (clone/sync with https://github.com/Causevest/archive, if necessary)

### 04. Edit/Create the Dockerfile. Use '0.0.0.0:80' or '0.0.0.0:5000' as ENV values based on the exposed port value in Dockerfile.
   Eg.
   EXPOSE 80
   ENV HOST '0.0.0.0'
   ENV PORT 80
   ENV MINER_ADDRESS ...

### 05. Do not forget to add the requirements.
   Eg. 
   RUN pip install --trusted-host pypi.python.org -r requirements.txt
   
### 06. In the tinycoin/src/app.py make sure of the following flask invocation.
   .run(str(host),int(port))
   
### 07. Build using the docker command
   $ docker build -t tinycoin .
   
### 08. Run using the docker command
   $ docker run -d -p 5000:80 tinycoin
   
### 09. Now access the tinycoin API like http://192.168.99.100:5000/blocks
   Note that the IP address provided by docker tool box is used here.
 
### 10. For IP tunneling, author used ngrok (https://ngrok.com/).
   Ngrok provides a command shell, in which a generated tunnel address is provided.
   Eg. a013d842.ngrok.io. 
   Use this for tinycoin API testing.

### 11. The tinycoin container should be manually stopped on Windows systems.
   $ docker container ls
                 Note down the name of the container from the above command.
   $ docker container stop <container name> 
   
### Extracts from the Dockerfile used by author for reference:
	
	FROM python:3.6-slim

	WORKDIR /app

	ADD . /app

	RUN pip install --trusted-host pypi.python.org -r requirements.txt

	EXPOSE 80

	ENV HOST '0.0.0.0'
	ENV PORT 80
	ENV MINER_ADDRESS '...'

	CMD ["python", "src/app.py"]

### Extract from src/app.py
	def getem(choice):
		ho = '0.0.0.0'
		po = 80
		ma = ''
		if(choice):
			j = json.load(open("./host.json", 'r'))
			name = j['name']
			ma = j['miner-address']
			ho = j['host']
			po = j['port']
		else:
			ma = os.getenv('MINER_ADDRESS','')
			ho = os.getenv('HOST','0.0.0.0')
			po = os.getenv('PORT',80)
		return(ma, ho, po)

	if __name__ == "__main__":
		print("Tinycoin server started ...!\n")
		(miner_address, host, port) = getem(False)
		print("MINER-ADDRESS: ", miner_address)
		print("         HOST: ", host)
		print("         PORT: ", port)
		
		node.run(str(host),int(port))

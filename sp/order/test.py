from ncclient import manager
import requests
import json



def acl(ip,user,passwd,permit,host,vendor,port):


	if vendor == 'cisco':
		try:
			url='http://{0}/ins'.format(ip)
			switchuser='{0}'.format(user)
			switchpassword='{0}'.format(passwd)

			myheaders={'content-type':'application/json'}
			payload={
			  "ins_api": {
			    "version": "1.0",
			    "type": "cli_conf",
			    "chunk": "0",
			    "sid": "1",
			    "input": "ip access-list AclTest ;permit ip {0} host {1}".format(permit,host),
			    "output_format": "json"
			  }
			}

			
			response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

		except:
			print 'pass nexus api cant be exucuted'
			pass

# def acl(ip,user,passwd,permit,host,vendor):

	elif vendor == 'juniper':
		try:
			username = user
			password = passwd
			ipv4 = ip
			port = port
			source = host
			destination = permit

			request_set_config_interface = """
			<config>
			  <configuration>
			    <firewall>
			        <filter>
			            <name>AclTest</name>
			            <term>
			                <name>1</name>
			                <from>
			                    <source-address>
			                        <name>{0}/32</name>
			                    </source-address>
			                    <destination-address>
			                        <name>{1}</name>
			                    </destination-address>
			                    <protocol>icmp</protocol>
			                </from>
			                <then>
			                    <accept/>
			                </then>
			            </term>
			        </filter>
			    </firewall>
			  </configuration>
			</config>
			""".format(source,destination)

			connection = manager.connect(host = ipv4, port = port, username = username, password = password, timeout = 20, device_params={'name':'junos'}, hostkey_verify=False )
			connection.edit_config(target='candidate', config=request_set_config_interface)
			connection.validate(source='candidate')
			connection.commit()

		except:
			print "junos netconf error"
			pass
! /bin/sh
#Test all endpoints of domain and return success/failure

function test {
   httpDomain="http://patrick-portfolio.duckdns.org"
   httpsDomain="https://patrick-portfolio.duckdns.org"
   declare -a endpoints=("" "health" "patrick" "athena" "juancarlos" "register" "login")

   #Generate random user and password
   username=$(date | md5sum)
   password=$(date | md5sum)

   for endpoint in "${endpoints[@]}"
   do
      url="${httpDomain}/${endpoint}"

      if [[ ${endpoint} == "register" ]]
      then
         curl -X POST -d "username=${username}&password=${password}" "${url}"
      elif [[ ${endpoint} == "login" ]]
      then
         curl -X POST -d "username=${username}&password=${password}" "${url}"
      else
         status=$(curl -s -o /dev/null -w "%{http_code}\n" "${url}")
         echo "Status Code [${status}] for ${url}"
      fi
   done
}

test

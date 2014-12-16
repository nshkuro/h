nodejs_npm 'coffee-script'

h_root = "/h"

bash "install elasticsearch-analysis-icu" do
  code <<-EOL  
  /usr/local/elasticsearch/bin/plugin -install elasticsearch/elasticsearch-analysis-icu/2.4.1
  EOL
end

bash "restart elasticsearch" do
  code <<-EOL  
  sudo service elasticsearch restart
  EOL
end

directory "#{h_root}" do
  action :create  
  mode "777"
  recursive true
end

git "#{h_root}" do
  repository "https://github.com/hypothesis/h.git"
  revision "master"
  action :sync  
end

bash "chmod" do
  code <<-EOL  
  chmod -R 777 /h
  EOL
end

template "#{h_root}/development.ini" do
  source "development.ini.erb"
  mode 0644
  variables(
    :host => "0.0.0.0",
  )  
end

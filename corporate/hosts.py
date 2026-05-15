from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'www', 'main.urls', name='main'),  
    host(r'dash', 'dash.urls', name='dash'), 

)
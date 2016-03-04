# polar
Content detection of the Polar Dataset

Due March 3, 2016


Instructions:
`pip install tika`


#Instructions for EMR Spark-Zeppelin-Python
- Start an EMR cluster with Spark 1.6.0, Hadoop and Zeppelin installed (you have to use the advanced settings page)
- Be sure to set TCP incoming and outgoing for SSH on 22 & TCP on 8890 both ways.
- Install boto3 via `sudo pip install boto3`
- Check out Zeppelin here: (note you will have to put in your Amazon IP.
`http://52.90.101.143:8890/`



#How to see our visualizations:
run `python -m http.server` in the main folder after cloning the repository to your local computer.
BFA:
`http://localhost:8000/BFA_Dhruv/d3_histograms/`
BFD:
`http://localhost:8000/bfd_json/atomXML.html` , as well as 
```
atomXML.html
difXML.html
octet_stream.html
pdf.html
rdfxml.html
rssxml.html
xhtmlXML.html
```
Mime Types that we chose in a barplot
`http://localhost:8000/mime_types_we_chose/`


We spent alot of time trying to get it set up with Spark, but had many issues with versioning and dependencies.
You can see our attempt code here:
`http://localhost:8000/zeppelin-spark/`

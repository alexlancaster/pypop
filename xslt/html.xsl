<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>

 <!-- select "html" as output method -->
 <xsl:output method="html" omit-xml-declaration="yes"/>

 <xsl:template match="/">
  <html>
   <pre>
    <xsl:apply-templates/> 
   </pre>
  </html>
 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

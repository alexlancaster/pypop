<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:output method="text" omit-xml-declaration="yes"/>

 <xsl:template match="/">
  <xsl:for-each select="dataanalysis/locus">
   <xsl:value-of select="substring-after(@name, '*')"/><xsl:text>: </xsl:text>
   <xsl:for-each select="allelecounts[@role!='no-data']/allele">
    <xsl:value-of select="@name"/>
    <xsl:text>/</xsl:text>
    <xsl:value-of select="count"/>
    <xsl:text> </xsl:text>
   </xsl:for-each>
<xsl:text>
</xsl:text>
  </xsl:for-each>
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


<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
  
  <xsl:variable name="all-allele-list" select="document('allelelist-by-locus.xml', .)/allelelist-by-locus"/>
  
 <xsl:template match="/">

  <xsl:for-each select="output/locus">
   
   <xsl:variable name="curlocus" select="@name"/>
   <xsl:variable name="allelelist-curlocus" select="$all-allele-list/locus[@name=$curlocus]"/>
    <xsl:text>     </xsl:text>
    <xsl:value-of select="count(population)"/>
    <xsl:text> </xsl:text>
    <xsl:text>1</xsl:text>
    <xsl:call-template name="newline"/>

   <xsl:for-each select="population">

    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar">
      <xsl:value-of select="popname"/>
     </xsl:with-param>
     <xsl:with-param name="length" select="9"/>
     </xsl:call-template>
    <xsl:text> </xsl:text>

    <xsl:variable name="cur-allele-list" select="allelecounts/allele"/>
       
    <xsl:for-each select="$allelelist-curlocus/allele">
      <xsl:variable name="allelename" select="."/>
      <xsl:choose>
       <xsl:when test="$cur-allele-list[@name=$allelename]">
        <xsl:value-of select="normalize-space($cur-allele-list[@name=$allelename]/frequency)"/>
       </xsl:when>
       <xsl:otherwise>0.00000</xsl:otherwise>
      </xsl:choose>
      <xsl:text> </xsl:text>
      </xsl:for-each>
      <xsl:call-template name="newline"/>
   </xsl:for-each>

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

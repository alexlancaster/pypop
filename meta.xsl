<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>
 
 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <xsl:template match="/">

  <xsl:for-each
   select="document(/meta/filename)/dataanalysis/locus">
   <xsl:for-each select=".">
    <xsl:value-of select="../filename"/>
    <xsl:text>:  </xsl:text>
    <xsl:value-of select="@name"/>
    <xsl:text>  </xsl:text>
    <xsl:choose>
     <xsl:when test="allelecounts/distinctalleles=''">0</xsl:when>
     <xsl:otherwise>
      <xsl:value-of select="allelecounts/distinctalleles"/>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="newline"/>
   </xsl:for-each>
  </xsl:for-each>
 </xsl:template>
 
 <!-- suppress output of random text -->
 <xsl:template match="text()">
  <!--  <xsl:value-of select="."/>  -->
 </xsl:template>


</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

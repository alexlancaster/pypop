<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
 
 <xsl:template match="/">

  <xsl:for-each select="output/locus">
   <xsl:variable name="kmax">
    <xsl:call-template name="max-value">
     <xsl:with-param name="path" select="population/allelecounts/distinctalleles"/>
    </xsl:call-template>
   </xsl:variable>
   
   <xsl:variable name="all-allele-names"
    select="population/allelecounts[distinctalleles=$kmax]/allele/@name"/>

   <xsl:variable name="locus-name" select="substring-after(@name, '*')"/>
   
   <xsl:text>&#09;</xsl:text>
   <xsl:value-of select="count(population[allelecounts[@role!='no-data']])"/>
   <xsl:call-template name="newline"/>

   <xsl:for-each select="population[allelecounts[@role!='no-data']]">

    <xsl:value-of select="substring(filename, 1, 10)"/>
    <xsl:text>&#09;</xsl:text>

    <xsl:variable name="allele-list" select="allelecounts/allele"/>

    <xsl:for-each select="$all-allele-names">
     <xsl:variable name="thename" select="."/>
     <xsl:choose>
      <xsl:when test="$allele-list[@name=$thename]">
       <xsl:value-of select="$allele-list[@name=$thename]/frequency"/>
      </xsl:when>
      <xsl:otherwise>0.000</xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>
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

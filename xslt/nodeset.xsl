<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 exclude-result-prefixes="exslt">

 <xsl:import href="sort-by-locus.xsl"/>
 <xsl:import href="lib.xsl"/>

 <xsl:template match="/">

  <xsl:variable name="sorted-by-locus">
   <xsl:call-template name="sort-by-locus"/>
  </xsl:variable>

  <xsl:variable name="all-alleles">
   <xsl:for-each select="exslt:node-set($sorted-by-locus)/output/locus">
    <locus>
     <xsl:attribute name="name"><xsl:value-of select="@name"/></xsl:attribute>
     <xsl:message><xsl:value-of select="@name"/></xsl:message>
     <xsl:variable name="kmax">
      <xsl:call-template name="max-value">
       <xsl:with-param name="path" select="population/allelecounts/distinctalleles"/>
      </xsl:call-template>
     </xsl:variable>
     <xsl:for-each select="population/allelecounts[distinctalleles=$kmax]/allele">
      <xsl:message><xsl:value-of select="@name"/></xsl:message>
     <allele><xsl:value-of select="@name"/></allele>
    </xsl:for-each>
    </locus>
   </xsl:for-each>
  </xsl:variable>
  
  <xsl:variable name="pops" select="/meta/dataanalysis"/>
  
  <xsl:value-of select="count($pops)"/>
  <xsl:text>     </xsl:text>
  
  <xsl:call-template name="newline"/>

  <xsl:for-each select="exslt:node-set($all-alleles)/locus">
   <xsl:if test="count(allele)">
    <xsl:value-of select="count(allele)"/>
   </xsl:if>
   <xsl:text> </xsl:text>
  </xsl:for-each>
  
  <xsl:call-template name="newline"/>

  <xsl:for-each select="$pops">
   
   <xsl:call-template name="append-pad">
    <xsl:with-param name="padVar">
     <xsl:value-of select="populationdata/popname"/>
     </xsl:with-param>
    <xsl:with-param name="length" select="9"/>
   </xsl:call-template>
   <xsl:text> </xsl:text>

   <xsl:for-each select="locus">
    <xsl:variable name="curlocus" select="@name"/>

    <xsl:variable name="allele-list" select="allelecounts/allele"/>
   
    <xsl:for-each select="exslt:node-set($all-alleles)/locus[@name=$curlocus]/allele">
     <xsl:variable name="allelename" select="."/>
     <xsl:choose>
      <xsl:when test="$allele-list[@name=$allelename]">
       <xsl:value-of select="$allele-list[@name=$allelename]/frequency"/>
      </xsl:when>
      <xsl:otherwise>0.000</xsl:otherwise>
     </xsl:choose>
     <xsl:text> </xsl:text>
    </xsl:for-each>
   </xsl:for-each>
   <xsl:call-template name="newline"/>
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

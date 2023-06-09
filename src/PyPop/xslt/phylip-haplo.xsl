<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 extension-element-prefixes="exslt"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" encoding="utf8" omit-xml-declaration="yes"/>

 <!-- specify a default directory for the output .dat files that can be overriden -->
 <xsl:param name="outputDir" select="'./'"/>

 <data:phylip-loci>
  <loci><locus>A</locus><locus>B</locus></loci>
  <loci><locus>B</locus><locus>C</locus></loci>
  <loci><locus>DRB1</locus><locus>DQB1</locus></loci>
  <loci><locus>A</locus><locus>B</locus><locus>DRB</locus></loci>
  <loci><locus>DRB1</locus><locus>DPB1</locus></loci>
 </data:phylip-loci>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
  
 <xsl:variable name="all-haplo-list" select="document('haplolist-by-group.xml', .)/haplolist-by-group"/>

 <xsl:template name="phylip-haplos">
  <xsl:param name="node"/>
  <xsl:param name="loci-to-output"/>

<!--
  <xsl:message>count: <xsl:value-of select="count($node)"/></xsl:message>
  <xsl:message><xsl:value-of select="name($node)"/></xsl:message>
  <xsl:message>loci to output: <xsl:value-of select="$loci-to-output"/></xsl:message>

-->

  <xsl:choose>
   <xsl:when test="count($node)=0">
    <xsl:variable name="warning-text">
    <xsl:value-of select="$loci-to-output"/>

     <xsl:text>: no populations have haplotype data for specified loci.</xsl:text>
    </xsl:variable>

    <xsl:value-of select="$warning-text"/>
    <xsl:message><xsl:value-of select="$warning-text"/></xsl:message>
   </xsl:when>

   <xsl:otherwise>

    <xsl:text>    </xsl:text>
    <xsl:value-of select="count($node)"/>
    <xsl:text> </xsl:text>
    <xsl:text>1</xsl:text>
    <xsl:call-template name="newline"/>
    
    <xsl:variable name="haplolist-curlocus"
     select="$all-haplo-list/group[@loci=$loci-to-output]"/>
    <xsl:value-of select="count($haplolist-curlocus/haplotype)"/>   
    <xsl:text> </xsl:text>
    
    <xsl:call-template name="newline"/>
    
    <xsl:for-each select="$node">
     
     <xsl:sort select="populationdata/popname"/>
     
     <xsl:call-template name="append-pad">
      <xsl:with-param name="padVar">
       <xsl:value-of select="populationdata/popname"/>
      </xsl:with-param>
      <xsl:with-param name="length" select="9"/>
     </xsl:call-template>
     <xsl:text> </xsl:text>
     
     <xsl:variable name="cur-haplo-list" select="emhaplofreq/group[@loci=$loci-to-output]/haplotypefreq/haplotype"/>
     
     <xsl:for-each select="$haplolist-curlocus/haplotype">
      <xsl:variable name="haplotype" select="."/>
      <xsl:choose>
       <xsl:when test="$cur-haplo-list[@name=$haplotype]">
	<xsl:value-of select="normalize-space($cur-haplo-list[@name=$haplotype]/frequency)"/>
       </xsl:when>
       <xsl:otherwise>0.00000</xsl:otherwise>
      </xsl:choose>
      <xsl:text> </xsl:text>
     </xsl:for-each>
     
     <xsl:call-template name="newline"/>
     
    </xsl:for-each>
   
   </xsl:otherwise>
  </xsl:choose>

 </xsl:template>

 <xsl:template name="genfile">
  <xsl:param name="filename"/>
  <xsl:param name="loci"/>
  
  <exslt:document href="{$outputDir}{$filename}"
   omit-xml-declaration="yes"
   method="text">
   <xsl:call-template name="phylip-haplos">
    <xsl:with-param name="node" select="//meta/dataanalysis[emhaplofreq/group/@loci=$loci]"/>
    <xsl:with-param name="loci-to-output" select="$loci"/>
   </xsl:call-template>
  </exslt:document>

 </xsl:template>

 <!-- loci to do haplos for, no default -->
 <xsl:param name="loci"/>
 
 <xsl:template match="/">

<!--
  <xsl:for-each select="document('')//data:phylip-loci/loci">

   <xsl:message>
    <xsl:value-of select="count(//meta/dataanalysis)"/>
   </xsl:message>

   <xsl:variable name="filename">
    <xsl:for-each select="locus">
     <xsl:value-of select="."/>
     <xsl:if test="position()!=last()">
      <xsl:text>-</xsl:text>
     </xsl:if>
    </xsl:for-each>
    <xsl:text>.haplo.phy</xsl:text>
   </xsl:variable>

   <xsl:variable name="loci">
    <xsl:for-each select="locus">
     <xsl:value-of select="."/>
     <xsl:if test="position()!=last()">
      <xsl:text>:</xsl:text>
     </xsl:if>
    </xsl:for-each>
   </xsl:variable>

   <xsl:call-template name="genfile">
    <xsl:with-param name="filename" select="$filename"/>
    <xsl:with-param name="loci" select="$loci"/>
   </xsl:call-template>

  </xsl:for-each>
-->

  <xsl:variable name="filename" select="concat(translate($loci, ':', '-'), '.haplo.phy')"/>

  <exslt:document href="{$outputDir}{$filename}"
   omit-xml-declaration="yes"
   method="text">
    <xsl:call-template name="phylip-haplos">
    <xsl:with-param name="node" select="//meta/dataanalysis[emhaplofreq/group[@loci=$loci and not(@role='no-data')]]"/>
    <xsl:with-param name="loci-to-output" select="$loci"/>
   </xsl:call-template>
  </exslt:document>
  
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

<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 extension-element-prefixes="exslt">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
  
  <xsl:variable name="all-allele-list" select="document('allelelist-by-locus.xml', .)/allelelist-by-locus"/>

 <xsl:template name="phylip-contents">
  <xsl:param name="node" select="."/>

  <xsl:variable name="curlocus" select="$node/@name"/>

  <xsl:variable name="allelelist-curlocus" select="$all-allele-list/locus[@name=$curlocus]"/>
  
  <xsl:text>     </xsl:text>
  <xsl:value-of select="count($node/population)"/>
  <xsl:text> </xsl:text>
  <xsl:text>1</xsl:text>
  <xsl:call-template name="newline"/>

  <xsl:value-of select="count($allelelist-curlocus/allele)"/>
  <xsl:call-template name="newline"/>

  <xsl:for-each select="$node/population">
   
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
 </xsl:template>
 
 <xsl:template match="/">
  
  <xsl:for-each select="output/locus">
   <xsl:variable name="locusname" select="@name"/>
   <xsl:if test="count($all-allele-list/locus[@name=$locusname]/allele)!=0">
    <xsl:variable name="filename" select="concat($locusname, '.phylip')"/>

    <exslt:document href="{$filename}"
     omit-xml-declaration="yes"
     method="text">
     <xsl:call-template name="phylip-contents">
     <xsl:with-param name="node" select="."/>
     </xsl:call-template>
    </exslt:document>
   </xsl:if>
  </xsl:for-each>

  <exslt:document href="2n-by-locus.dat"
   omit-xml-declaration="yes"
   method="text">
   <xsl:for-each select="output/locus">
    <xsl:text>Locus: </xsl:text>
    <xsl:value-of select="@name"/>
    <xsl:call-template name="newline"/>
    
    <xsl:for-each select="population">
     <xsl:text>  </xsl:text>
     <xsl:value-of select="popname"/><xsl:text> ('</xsl:text><xsl:value-of select="filename"/><xsl:text>'): </xsl:text>
     <xsl:choose>
      <xsl:when test="allelecounts/allelecount">
       <xsl:value-of select="allelecounts/allelecount"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>
     <xsl:call-template name="newline"/>
    </xsl:for-each>
   </xsl:for-each>  
  </exslt:document>

  <!--  
  <xsl:for-each select="output/locus">
   <xsl:call-template name="phylip-contents">
    <xsl:with-param name="node" select="."/>
   </xsl:call-template>
  </xsl:for-each>
  -->
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

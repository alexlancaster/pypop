<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>
 
 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <!-- unique key for all loci -->
 <xsl:key name="loci" match="/meta/dataanalysis/locus" use="@name"/>

 <xsl:template match="/">

<!--

old-style: search

  <xsl:for-each
   select="/meta/dataanalysis/locus">
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
-->

  <xsl:call-template name="newline"/>

  <xsl:variable name="names"
   select="/meta/dataanalysis/locus[generate-id(.)=generate-id(key('loci',@name))]"/>
  
  <xsl:for-each select="$names">
   <xsl:call-template name="prepend-pad">
    <xsl:with-param name="padVar" select="@name"/>
    <xsl:with-param name="length" select="7"/>
   </xsl:call-template>
  </xsl:for-each>

  <xsl:call-template name="newline"/>

  <xsl:for-each
   select="/meta/dataanalysis">
   <xsl:sort select="@date"/>
   <xsl:value-of select="@date"/>-<xsl:value-of select="filename"/>

   <xsl:variable name="curr-node" select="."/>

   <xsl:call-template name="newline"/>

   <xsl:for-each select="$names/@name">
    <xsl:variable name="attr">
     <xsl:value-of select="."/>
    </xsl:variable>

    <xsl:variable name="cell">
     <xsl:choose>
      <xsl:when
       test="$curr-node/locus[@name=$attr]/allelecounts/distinctalleles">
       <xsl:value-of select="$curr-node/locus[@name=$attr]/allelecounts/distinctalleles"/>
      </xsl:when>
      <xsl:otherwise>
       <xsl:text>0</xsl:text>
      </xsl:otherwise>
     </xsl:choose>
    </xsl:variable>

    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padVar" select="$cell"/>
     <xsl:with-param name="length" select="7"/>
    </xsl:call-template>
    
   </xsl:for-each>

   <xsl:call-template name="newline"/>
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
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

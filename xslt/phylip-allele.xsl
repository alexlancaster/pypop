<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 extension-element-prefixes="exslt"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <data:phylip-loci>
  <loci><locus>A</locus><locus>B</locus></loci>
  <loci><locus>B</locus><locus>C</locus></loci>
  <loci><locus>DRB1</locus><locus>DQB1</locus></loci>
  <loci><locus>A</locus><locus>B</locus><locus>DRB</locus></loci>
  <loci><locus>DRB1</locus><locus>DPB1</locus></loci>
 </data:phylip-loci>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
  
 <xsl:variable name="all-allele-list" select="document('allelelist-by-locus.xml', .)/allelelist-by-locus"/>
 
 <xsl:template name="phylip-alleles">
  <xsl:param name="node"/>

  <xsl:variable name="loci" select="$node/@name"/>

  <xsl:variable name="loci-count" select="count($loci)"/>
  
  <xsl:variable name="unique-pops" select="//popname[not(.=following::popname)]" />   

  <xsl:variable name="populations_alldata" select="$node/population[not(allelecounts/@role='no-data')]"/>

  <xsl:variable name="populations" select="$unique-pops[count($populations_alldata[popname])=$loci-count]"/>


  <xsl:message>
   <xsl:for-each select="$unique-pops">
    <xsl:value-of select="."/>
    <xsl:text>: </xsl:text>
    <xsl:value-of select="count($populations_alldata[current()=popname])=$loci-count"/>
    <xsl:text>, </xsl:text>
   </xsl:for-each>

   <xsl:value-of select="count($populations)"/>

   <xsl:value-of select="$populations"/>
   
  </xsl:message>

<!--  <xsl:variable name="populations" select="$all-populations"/> -->

<!--
  <xsl:variable name="populations" select="$all-populations[not(popname=preceding-sibling::popname)]/popname"/> 
-->

  <xsl:text>     </xsl:text>
  <xsl:value-of select="count($populations)"/>
  <xsl:text> </xsl:text>
  <xsl:value-of select="count($loci)"/>
  <xsl:call-template name="newline"/>

  <xsl:for-each select="$loci">
   <xsl:variable name="curlocus" select="."/>

   <xsl:variable name="allelelist-curlocus"
    select="$all-allele-list/locus[@name=$curlocus]"/>
   
   <xsl:value-of select="count($allelelist-curlocus/allele)"/>   
   <xsl:text> </xsl:text>
  </xsl:for-each>
  
  <xsl:call-template name="newline"/>
  
  <xsl:for-each select="$populations">

   <xsl:sort select="."/>
   
   <xsl:variable name="curpop" select="."/>
   
   <xsl:call-template name="append-pad">
    <xsl:with-param name="padVar">
     <xsl:value-of select="$curpop"/>
    </xsl:with-param>
    <xsl:with-param name="length" select="9"/>
   </xsl:call-template>
   <xsl:text> </xsl:text>
   
   <xsl:for-each select="$loci">
    
    <xsl:variable name="curlocus" select="."/>
    
    <xsl:variable name="allelelist-curlocus"
     select="$all-allele-list/locus[@name=$curlocus]"/>
    
    <xsl:variable name="cur-allele-list" select="$node[@name=$curlocus]/population[popname=$curpop]/allelecounts/allele"/>
    
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
    
   </xsl:for-each>
   
   <xsl:call-template name="newline"/>
  </xsl:for-each>
 </xsl:template>

 <!-- loci to group, no default -->
 <xsl:param name="loci"/>
 
 <xsl:template match="/">

  <xsl:variable name="filename" select="concat(translate($loci, ':', '-'), '.allele.phy')"/>

  <xsl:choose>
   <xsl:when test="$loci">
    <!-- a parameter is passed in, do those specified loci -->

    <exslt:document href="{$filename}"
     omit-xml-declaration="yes"
     method="text">
     <xsl:call-template name="phylip-alleles">
      <xsl:with-param name="node" select="output/locus[contains($loci, @name)]"/>
     </xsl:call-template>
    </exslt:document>
   </xsl:when>

   <xsl:otherwise>
    <!-- otherwise, do all pairs -->

    <xsl:for-each select="output/locus">
     <xsl:variable name="locusname" select="@name"/>
     <xsl:if test="count($all-allele-list/locus[@name=$locusname]/allele)!=0">
      <xsl:variable name="filename" select="concat($locusname, '.allele.phy')"/>
      <exslt:document href="{$filename}"
       omit-xml-declaration="yes"
       method="text">
       <xsl:call-template name="phylip-alleles">
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
   </xsl:otherwise>
  </xsl:choose>

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

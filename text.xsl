<!DOCTYPE xsl:stylesheet SYSTEM "xsl.dtd">
<xsl:stylesheet version='1.0' xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- select "text" as output method -->
 <xsl:output method="text"/>
 
 <xsl:template match="/">
  <xsl:apply-templates/>
 </xsl:template>
 
 <!-- suppress output of random text -->
 <xsl:template match="text()">
  <!--  <xsl:value-of select="."/>  -->
 </xsl:template>

 <!-- BEGIN NAMED TEMPLATE FUNCTIONS -->
 
 <xsl:template name="prepend-pad"> 
  <!-- recursive template to right justify and prepend-->
  <!-- the value with whatever padChar is passed in   -->
  <xsl:param name="padChar"> </xsl:param>
  <xsl:param name="padVar"/>
  <xsl:param name="length"/>
  <xsl:choose>
   <xsl:when test="string-length($padVar) &lt; $length">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padChar" select="$padChar"/>
     <xsl:with-param name="padVar" select="concat($padChar,$padVar)"/>
     <xsl:with-param name="length" select="$length"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of 
     select="substring($padVar,string-length($padVar) -
     $length + 1)"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>
 
 <xsl:template name="append-pad">
  <!-- recursive template to left justify and append  -->
  <!-- the value with whatever padChar is passed in   -->
  <xsl:param name="padChar"> </xsl:param>
  <xsl:param name="padVar"/>
  <xsl:param name="length"/>
  <xsl:choose>
   <xsl:when test="string-length($padVar) &lt; $length">
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padChar" select="$padChar"/>
     <xsl:with-param name="padVar" select="concat($padVar,$padChar)"/>
     <xsl:with-param name="length" select="$length"/>
    </xsl:call-template>
   </xsl:when>
   <xsl:otherwise>
    <xsl:value-of select="substring($padVar,1,$length)"/>
   </xsl:otherwise>
  </xsl:choose>
 </xsl:template>

 <!-- prints a newline -->
 <xsl:template name="newline"><xsl:text>
  </xsl:text></xsl:template>

 <!-- formats a header: a "title" underlined with equals-signs (`=') -->
 <xsl:template name="header">
  <xsl:param name="title"/>
  <xsl:value-of select="$title"/>
  <xsl:call-template name="newline"/>
  <xsl:call-template name="append-pad">
   <xsl:with-param name="padChar" select="'='"/>
   <xsl:with-param name="length" select="string-length($title)"/>
  </xsl:call-template>
  <xsl:call-template name="newline">
  </xsl:call-template>
 </xsl:template>

 <!-- formats a list of nodes which are fields in name: value format
 separated by newlines -->
 <xsl:template name="linesep-fields">
  <xsl:param name="nodes" select="*"/>
  <xsl:for-each select="$nodes">
   <xsl:text>*</xsl:text>
   <xsl:value-of select="name(.)"/>
   <xsl:text>*: </xsl:text>
   <xsl:value-of select="."/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>
 </xsl:template> 

 <!-- END NAMED TEMPLATE FUNCTIONS -->
 
 <!-- BEGIN MATCH TEMPLATE FUNCTIONS -->

 <!-- top-level element -->
 <!-- start processing here -->
 <xsl:template match="dataanalysis">
  <xsl:text>Results of data analysis</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:text>Performed on the '</xsl:text><xsl:value-of select="filename"/><xsl:text>' file at: </xsl:text><xsl:value-of select="@date"/>
  <xsl:call-template name="newline"/>
  <xsl:call-template name="newline"/>

  <!-- print out population-level statistics and information -->
  <xsl:apply-templates select="filename|populationdata"/>

  <!-- loop through each locus in turn -->
  <xsl:for-each select="locus">

   <!-- print each locus name -->
   <xsl:call-template name="header">
    <xsl:with-param name="title">Locus:<xsl:value-of select="@name"/></xsl:with-param>
   </xsl:call-template>
   <xsl:call-template name="newline"/>

   <xsl:choose>
    <!-- if allele data is present output the subnodes -->
    <xsl:when test="allelecounts/@role!='no-data'">
     <xsl:apply-templates select="*"/>
    </xsl:when>
    <!-- if no allele data is present supress processing and print message -->
    <xsl:otherwise>
     <xsl:text> No data for this locus!</xsl:text>
     <xsl:call-template name="newline"/>
    </xsl:otherwise>
   </xsl:choose>
   <xsl:call-template name="newline"/>
  </xsl:for-each>
 </xsl:template>
 
 <!-- leave filename blank, this is output in a different context  -->
 <xsl:template match="filename"/>
 
 <!-- metadata `header' block -->
 <xsl:template match="populationdata">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Population Summary</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
 </xsl:template>
 
 <xsl:template match="longitude|latitude|ethnicgroup|collectionsite|typingmethod|continentoforigin|labcode">
  <xsl:text>*</xsl:text>
  <xsl:value-of select="name(.)"/>
  <xsl:text>*: </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
  </xsl:template>
 
 <!-- metadata totals -->
 <xsl:template match="populationdata/totals">
  <xsl:call-template name="newline"/>
  <xsl:call-template name="header">
   <xsl:with-param name="title">Population Totals</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
  <xsl:call-template name="newline"/>
 </xsl:template>
 
 <!-- these next 3 templates print out the same data which can be used
 in different contexts: both for population-level stats and individual
 loci -->

 <xsl:template match="indivcount">
  <xsl:text>Sample Size (n): </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>
 
 <xsl:template match="allelecount">
  <xsl:text>Allele Count (2n): </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>
 
 <xsl:template match="locuscount">
  <xsl:text>Total Loci: </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="untypedindividuals">
  <xsl:text>Untyped individuals: </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- Allele count statistics --> 
 <xsl:template match="allelecounts">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Allele Counts [<xsl:value-of select="../@name"/>]</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:choose>
  
   <!-- if there's no data, don't do anything -->
   <xsl:when test="@role='no-data'">
    <xsl:text>No allele data!</xsl:text>
    <xsl:call-template name="newline"/>
   </xsl:when>
   
   <xsl:otherwise>
    <!-- do all the non-allelecount templates -->
    <xsl:apply-templates select="*[not(self::allele)]"/>

    <!-- create a header for table -->
    <xsl:text>Name   Frequency  (Count)</xsl:text>
    <xsl:call-template name="newline"/>
    
    <!-- loop through each allele-->
    <xsl:for-each select="allele">
     <xsl:value-of select="@name"/><xsl:text> </xsl:text>
     <xsl:value-of select="frequency"/><xsl:text> </xsl:text>
     <xsl:text>(</xsl:text><xsl:value-of select="count"/><xsl:text>)</xsl:text>
     <xsl:call-template name="newline"/>
    </xsl:for-each>
    
    <!-- print out the total at end of table -->
    <xsl:text>Total frequency: </xsl:text><xsl:value-of
     select="totalfrequency"/><xsl:text> (</xsl:text><xsl:value-of
     select="totalcount"/><xsl:text>)</xsl:text>
    <xsl:call-template name="newline"/>

   </xsl:otherwise>
  </xsl:choose>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- HardyWeinberg statistics -->
 <xsl:template match="hardyweinberg">
  <xsl:call-template name="header">
   <xsl:with-param name="title">HardyWeinberg [<xsl:value-of select="../@name"/>]</xsl:with-param>
  </xsl:call-template>

  <xsl:choose>

   <xsl:when test="@role='lumps'">
    <xsl:call-template name="newline"/>
    <xsl:text>*Lumped output*</xsl:text>
    <xsl:call-template name="newline"/>
<!--    <xsl:apply-templates select="*[not(self::allele)]"/> -->
    <xsl:call-template name="linesep-fields">
     <xsl:with-param name="nodes" select="*"/>
    </xsl:call-template>
   </xsl:when>

   <xsl:when test="@role='no-common-genotypes'">
    <xsl:text>*No common genotypes, no output!*</xsl:text>
    <xsl:call-template name="newline"/>
   </xsl:when>

   <xsl:otherwise>
    <xsl:message>Error! hardyweinberg tag must have a 'class'
     attribute</xsl:message>
   </xsl:otherwise>
  </xsl:choose>

  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- Homozygosity statistics --> 
 <xsl:template match="homozygosity">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Homozygosity [<xsl:value-of select="../@name"/>]</xsl:with-param>
  </xsl:call-template>
  
  <xsl:choose>

   <xsl:when test="@role='out-of-range'">
    <xsl:text>*Out of range of simulated homozygosity values*</xsl:text>
    <xsl:call-template name="newline"/>
    <xsl:text>*can't estimate expected homozygosity*</xsl:text>
   </xsl:when>

   <xsl:otherwise>
    <xsl:call-template name="newline"/>

    <!-- print out all lineseparated fields, except pvalue -->
    <xsl:call-template name="linesep-fields">
     <xsl:with-param name="nodes" select="*[not(self::pvalue)]"/>
    </xsl:call-template>

    <!-- treat pvalue differently, since it is not a simple value, but
    has an upper and lower bound -->

    <xsl:value-of select="pvalue/lower"/> <xsl:text>&lt; *pvalue* &lt; </xsl:text><xsl:value-of select="pvalue/upper"/>
    <xsl:call-template name="newline"/>
   </xsl:otherwise>

  </xsl:choose>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- END MATCH TEMPLATE FUNCTIONS -->

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
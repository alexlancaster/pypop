<xsl:stylesheet version='1.0' xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>
 
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
  <xsl:param name="padChar" select="' '"/>
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
  <!-- <xsl:param name="padChar"> </xsl:param> -->
  <xsl:param name="padChar" select="' '"/>
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
 
  <!-- if field has any attribute, print them out in brackets
   separated by commas -->
   
   <xsl:if test="@*!=''">
    <xsl:text> (</xsl:text>
    <xsl:for-each select="@*">
     <xsl:value-of select="."/>
     <xsl:if test="position()!=last()">
      <xsl:text>, </xsl:text>
     </xsl:if>
     </xsl:for-each>
    <xsl:text>)</xsl:text>
   </xsl:if>
   
   <xsl:call-template name="newline"/>

  </xsl:for-each>
 </xsl:template> 

 <!-- finds the maximum string length of a set of elements, found in
 the `path' variable -->
 <xsl:template name="max-string-len">
  <xsl:param name="path" select="."/>
  <xsl:for-each select="$path">
   <xsl:sort select="string-length(.)" data-type="number" order="descending"/>
   <xsl:if test="position()=1">
    <xsl:value-of select="string-length(.)"/></xsl:if>
  </xsl:for-each>
 </xsl:template>

 <!-- END NAMED TEMPLATE FUNCTIONS -->
 
 <!-- BEGIN MATCH TEMPLATE FUNCTIONS -->
 
 <!-- TOP-LEVEL ELEMENT -->
 <!-- START PROCESSING HERE -->
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

  <!-- Print out whole population-levels stats, such as --> 
  <!-- estimation of haplotypes and LD -->
  <xsl:apply-templates select="emhaplofreq"/>

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
  <xsl:call-template name="newline"/>

  <xsl:apply-templates
   select="common|lumped|heterozygotes|homozygotes"/>
  
  <!-- now do genotype table -->
  <xsl:apply-templates select="genotypetable"/>

  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="common|lumped|heterozygotes|homozygotes">

  <xsl:text>*</xsl:text>
  <xsl:value-of select="name(.)"/>
  <xsl:text>*: </xsl:text>
  <xsl:call-template name="newline"/>
  
  <xsl:choose>
   <xsl:when test="*!=''">
    <!-- when the tag has content -->
    <xsl:call-template name="linesep-fields">
     <xsl:with-param name="nodes" select="*"/>
    </xsl:call-template>
    <xsl:call-template name="newline"/>

   </xsl:when>

   <!-- if the tag does not have content, print the role attribute
   (will do more parsing of this for error messages later) -->
   <xsl:when test="*=''">
    <xsl:value-of select="@role"/>
    <xsl:call-template name="newline"/>
   </xsl:when>

   <!-- an "assert" message to test XSLT is working -->
   <xsl:otherwise>
    <xsl:message>Error! Output XML condition not covered!</xsl:message>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable">

  <xsl:variable name="padding" select="8"/>

  <xsl:variable name="row-len-max">
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="genotype/@row"/>
   </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="col-len-max">
   <xsl:call-template name="max-string-len">
    <xsl:with-param name="path" select="genotype/@col"/>
   </xsl:call-template>
  </xsl:variable>
  
  <xsl:for-each select="genotype">
   <xsl:sort select="@row"/>
   <xsl:if test="@row!=preceding-sibling::genotype/@row">
    <xsl:call-template name="newline"/>
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$row-len-max"/>
     <xsl:with-param name="padVar" select="@row"/>
    </xsl:call-template>
   </xsl:if>

   <xsl:for-each select="@col">
    <xsl:sort select="."/>
    <xsl:variable name="cell">
     <xsl:value-of select="../observed"/><xsl:text>/</xsl:text><xsl:value-of select="../expected"/>
    </xsl:variable>
    
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$padding"/>
     <xsl:with-param name="padVar" select="$cell"/>
    </xsl:call-template>
    
   </xsl:for-each>
  </xsl:for-each>

  <xsl:call-template name="newline"/>

  <!-- indent row for column names-->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$row-len-max"/>
  </xsl:call-template>

  <xsl:for-each select="genotype">
   <xsl:sort select="@col"/>

   <xsl:if test="@col!=preceding-sibling::genotype/@col">

    <xsl:variable name="footercell">
     <xsl:value-of select="@col"/>
    </xsl:variable>

    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="length" select="$padding"/>
     <xsl:with-param name="padVar" select="$footercell"/>
    </xsl:call-template>
    
   </xsl:if>
  </xsl:for-each>

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

    <xsl:value-of select="pvalue/lower" disable-output-escaping="yes"/><xsl:text disable-output-escaping="yes"> &lt; *pvalue* &lt; </xsl:text><xsl:value-of select="pvalue/upper" disable-output-escaping="yes"/>
    <xsl:call-template name="newline"/>
   </xsl:otherwise>

  </xsl:choose>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- Haplotype/LD statistics --> 
 <xsl:template match="emhaplofreq">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype/LD stats via emhaplofreq: <xsl:value-of select="../@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='haplo']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">No data left after filtering at: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='haplo']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>

  <!-- until output is XML-fied, simply pass through the unmarked
  CDATA section -->
  <xsl:value-of select="haplotypefreq" disable-output-escaping="yes"/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='LD']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">LD est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>


  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <!-- until output is XML-fied, simply pass through the unmarked
  CDATA section -->
  <xsl:value-of select="permutation" disable-output-escaping="yes"/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- END MATCH TEMPLATE FUNCTIONS -->
 
</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->

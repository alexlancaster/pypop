<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- boiler-plate text that we may want to re-use -->
 <data:hardyweinberg-col-headers>
  <text>Observed</text>
  <text>Expected</text>
  <text>Chi-square</text>
  <text>p-value</text>
  <text>d.o.f.</text>
 </data:hardyweinberg-col-headers>

 <!-- lookup table to translate population metadata XML tag names back
 to human-readable output -->
 <data:pop-col-headers>
  <text col="labcode">Lab code</text>
  <text col="method">Typing method</text>
  <text col="ethnic">Ethnicity</text>
  <text col="contin">Continent</text>
  <text col="collect">Collection site</text>
  <text col="latit">Latitude</text>
  <text col="longit">Longitude</text>
 </data:pop-col-headers>

 <xsl:param name="hardyweinberg-col-width" select="12"/>
 <xsl:param name="hardyweinberg-first-col-width"
 select="$hardyweinberg-col-width + 6"/>

 <xsl:template match="/">
  <xsl:apply-templates/> 
 </xsl:template>
 
 <!-- suppress output of random text -->
 <xsl:template match="text()">
  <!--  <xsl:value-of select="."/>  -->
 </xsl:template>
 
 <!-- BEGIN NAMED TEMPLATE FUNCTIONS -->

 <xsl:template name="get-significance">
  <xsl:param name="pvalue"/>
  <xsl:choose>
   <xsl:when test="$pvalue &lt;= 0.00001">5</xsl:when>
   <xsl:when test="$pvalue &lt;= 0.0001">4</xsl:when>
   <xsl:when test="$pvalue &lt;= 0.001">3</xsl:when>
   <xsl:when test="$pvalue &lt;= 0.01">2</xsl:when>
   <xsl:when test="$pvalue &lt;= 0.05">1</xsl:when>
   <xsl:otherwise>0</xsl:otherwise>
  </xsl:choose>

 </xsl:template>

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

 <!-- formats a "locus" header, given a title and then gets the -->
 <!-- locus name from the "name" attribute in the parent context node -->
 <xsl:template name="locus-header">
  <xsl:param name="title"/>
  <xsl:call-template name="header">
   <xsl:with-param name="title"><xsl:value-of select="$title"/> [<xsl:value-of select="../@name"/>]</xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <!-- formats a list of nodes which are fields in name: value format
 separated by newlines -->
 <xsl:template name="linesep-fields">
  <xsl:param name="nodes" select="*"/>
  <xsl:for-each select="$nodes">
   <xsl:text></xsl:text>
   <xsl:value-of select="name(.)"/>
   <xsl:text>: </xsl:text>

   <xsl:choose>
    <xsl:when test="name(.)='pvalue'">
     <xsl:apply-templates select="."/>
    </xsl:when>
    <xsl:otherwise>
     <xsl:value-of select="."/> 
    </xsl:otherwise>
   </xsl:choose>

 
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

 <!-- END NAMED TEMPLATE FUNCTIONS -->
 
 <!-- BEGIN MATCH TEMPLATE FUNCTIONS -->
 

 <!-- ####################  METADATA OUTPUT ###################### -->  

 <!-- TOP-LEVEL XML ELEMENT -->

 <xsl:template match="dataanalysis">
  <xsl:text>Results of data analysis</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:text>Performed on the '</xsl:text><xsl:value-of select="filename"/><xsl:text>' file at: </xsl:text><xsl:value-of select="@date"/>
  <xsl:call-template name="newline"/>
  <xsl:call-template name="newline"/>

 <!-- ####################  END METADATA OUTPUT ###################### -->  

 <!-- ####################  POPULATION OUTPUT ######################## -->  
  
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

 <!-- pre-calculate the maximum length of the metadata text
 length to use in padding for the population summary -->
 <xsl:param name="metadata-max-len">
  <xsl:call-template name="max-string-len">
   <xsl:with-param name="path" 
    select="document('')//data:pop-col-headers/text"/>
  </xsl:call-template>
 </xsl:param>

 <xsl:template match="longit|latit|ethnic|collect|method|contin|labcode">

  <!-- store the current node name for the lookup-table -->
  <xsl:variable name="node-name" select="name(.)"/>

  <!-- use the lookup-table to get the verbose (human-readable)
  version of the metadata element -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="padVar">
    <xsl:value-of 
     select="document('')//data:pop-col-headers/text[@col=$node-name]"/>  
   </xsl:with-param>
   <xsl:with-param name="length" select="$metadata-max-len"/>
  </xsl:call-template>
  <xsl:text>: </xsl:text>
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
  <xsl:text>Total Loci in file: </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="lociWithDataCount">
  <xsl:text>Total Loci with data: </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="untypedindividuals">
  <xsl:text>Untyped individuals: </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="distinctalleles">
  <xsl:text>Distinct alleles (k): </xsl:text>
  <xsl:value-of select="."/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- ####################  END POPULATION OUTPUT ##################### -->  

 <!-- #################  ALLELE COUNT STATISTICS ###################### --> 
 
 <xsl:template match="allelecounts">
  <xsl:call-template name="locus-header">
   <xsl:with-param name="title">Allele Counts</xsl:with-param>
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

    <xsl:call-template name="newline"/>

    <!-- create a header for table -->
    <xsl:text>Name      Frequency (Count)</xsl:text>
    <xsl:call-template name="newline"/>
    
    <!-- loop through each allele-->
    <xsl:for-each select="allele">
     <xsl:sort select="count" data-type="number" order="descending"/>
     <xsl:for-each select="frequency|count|@name">
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="."/>
       <xsl:with-param name="length">10</xsl:with-param>
      </xsl:call-template>
     </xsl:for-each>
     <xsl:call-template name="newline"/>
    </xsl:for-each>
    
    <!-- print out the totals at end of table -->
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar">Total</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
    </xsl:call-template>
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="totalfrequency"/>
     <xsl:with-param name="length" select="10"/>
    </xsl:call-template>
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="totalcount"/>
     <xsl:with-param name="length" select="10"/>
    </xsl:call-template>
    <xsl:call-template name="newline"/>

   </xsl:otherwise>
  </xsl:choose>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- ############### END ALLELE COUNT STATISTICS ###################### --> 

 <!-- ################  HARDY-WEINBERG STATISTICS ###################### --> 

 <xsl:template match="hardyweinberg">
  <xsl:call-template name="locus-header">
   <xsl:with-param name="title">HardyWeinberg</xsl:with-param>
  </xsl:call-template>

  <!-- do genotype table -->
  <xsl:apply-templates select="genotypetable"/>

  <xsl:call-template name="newline"/>

  <!-- indent first line of table -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
  </xsl:call-template>

  <!-- print header for the individual stats -->
  <xsl:for-each select="document('')//data:hardyweinberg-col-headers/text">
    <xsl:call-template name="prepend-pad">
     <xsl:with-param name="padVar" select="."/>
     <xsl:with-param name="length" select="$hardyweinberg-col-width"/>
    </xsl:call-template>
  </xsl:for-each>

  <!-- separator -->
  <xsl:call-template name="newline"/>
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

  <!-- no do individual stats for each class -->
  <xsl:apply-templates select="common"/>
  <xsl:apply-templates select="lumped"/>
  <xsl:apply-templates select="commonpluslumped"/>
  <xsl:apply-templates select="heterozygotes|homozygotes"/>

  <!-- do stats for all the heterozygotes and genotypes -->
  <xsl:apply-templates select="heterozygotesByAllele"/>

  <xsl:apply-templates select="genotypetable" mode="genotypesByGenotype"/>
  
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- template to generate the (padded) cell ;-) -->
 <!-- this also handles the case when there is no tag because it -->
 <!-- will simply return a white-space padded cell of the right length -->
 <xsl:template name="hardyweinberg-gen-cell">
  <xsl:param name="node" select="."/>
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="padVar" select="$node"/>
   <xsl:with-param name="length" select="$hardyweinberg-col-width"/>
  </xsl:call-template>
 </xsl:template>

 <!-- template to generate the row -->
 <xsl:template name="hardyweinberg-gen-row">
  
  <!-- create variables from the contents of the cells  -->
  <xsl:variable name="observed">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="observed"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="expected">
   <!-- for this column only, round the expected to 2 decimal places -->
   <xsl:variable name="expected-rounded">
    <xsl:call-template name="round-to">
     <xsl:with-param name="node" select="expected"/>
     <xsl:with-param name="places" select="2"/>
    </xsl:call-template>
   </xsl:variable>
   <!-- then pass this new value to the generate the table cell -->
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="$expected-rounded"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="chisq">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="chisq"/>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="pvalue">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node">
     <xsl:apply-templates select="pvalue"/>
    </xsl:with-param>
   </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="chisqdf">
   <xsl:call-template name="hardyweinberg-gen-cell">
    <xsl:with-param name="node" select="chisqdf"/>
   </xsl:call-template>
  </xsl:variable>

  <!-- concatenate all the cells -->
  <xsl:value-of select="concat($observed,$expected,$chisq,$pvalue,$chisqdf)"/>

 </xsl:template>

 <!-- print out overall HW stats  -->
 <xsl:template match="common|lumped|commonpluslumped|heterozygotes|homozygotes">

 <xsl:variable name="type">
   <xsl:choose>
    <xsl:when test="name(.)='homozygotes'">All homozygotes</xsl:when>
    <xsl:when test="name(.)='heterozygotes'">All heterozygotes</xsl:when>
    <xsl:when test="name(.)='common'">Common</xsl:when>
    <xsl:when test="name(.)='commonpluslumped'">Common + lumped</xsl:when>
    <xsl:when test="name(.)='lumped'">Lumped genotypes</xsl:when>
    <xsl:otherwise>
     <xsl:message terminate="yes">Should always match something</xsl:message>
    </xsl:otherwise>
   </xsl:choose>
 </xsl:variable>


  <!-- indent table -->
  <xsl:call-template name="prepend-pad">
   <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
   <xsl:with-param name="padVar" select="$type"/>
  </xsl:call-template>
  
  <xsl:choose>
   
   <xsl:when test="*!=''">
    <!-- when the tag has content generate the row -->
    <xsl:call-template name="hardyweinberg-gen-row"/>
   </xsl:when>

   <!-- if the tag does not have content, generate a diagnostic message -->
   <!-- based on the 'role' attribute -->
   <xsl:when test="*=''">

    <!-- make an extra space, for case when following text is flush left -->
    <xsl:text> </xsl:text>
  
    <xsl:choose>
     <xsl:when test="@role='too-many-parameters'">
      <xsl:text>
       Overall chi-square for common genotypes cannot be calculated due to
       too many parameter estimates (allele frequencies) for the number of
       common genotypes, leading to zero or negative degrees of freedom.
       This may by remedied by combining rare alleles and recalculating
       overall chi-square value and degrees of freedom.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='no-common-genotypes'">
      <xsl:text>No commmon genotypes; chi-square cannot be calculated</xsl:text>
     </xsl:when>
     <xsl:when test="@role='no-rare-genotypes'">
      <xsl:text>No rare genotypes with expected less than </xsl:text>
      <xsl:value-of select="../lumpBelow"/><xsl:text> was observed.</xsl:text>
     </xsl:when>
     <xsl:when test="@role='too-few-expected'">
      <xsl:text>
       There are less than </xsl:text><xsl:value-of
       select="../lumpBelow"/><xsl:text> genotypes with a value of at least </xsl:text><xsl:value-of select="../lumpBelow"/></xsl:when>
     </xsl:when>
     <xsl:whem test="@role='huh'">
      <xsl:text>Unhandled logical path through Hardy-Weinberg.</xsl:text>
     <xsl:otherwise>
      <xsl:text>Condition: </xsl:text><xsl:value-of
       select="@role"/><xsl:text> not recognized.</xsl:text>
     </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="newline"/>
   </xsl:when>

   <!-- an "assert" message to test XSLT is working -->
   <xsl:otherwise>
    <xsl:message>Error! Output XML condition not covered!</xsl:message>
   </xsl:otherwise>
  </xsl:choose>
  <xsl:call-template name="newline"/>

  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- print out info on heterozygotes and genotypes -->
 <xsl:template match="heterozygotesByAllele">
  <xsl:text>Heterozygotes by allele</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:for-each select="allele">
   
   <!-- sort by allele name -->
   <xsl:sort select="@name" data-type="text"/>
   <!-- indent table with name of the allele -->
   <xsl:call-template name="prepend-pad">
    <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    <xsl:with-param name="padVar" select="@name"/>
   </xsl:call-template>
   <!-- generate the row -->
   <xsl:call-template name="hardyweinberg-gen-row"/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>  

  <xsl:call-template name="newline"/>
  
  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable" mode="genotypesByGenotype">
  <xsl:text>Genotypes by genotype</xsl:text>
  <xsl:call-template name="newline"/>

  <!-- find all genotypes that have chisq set -->
  <xsl:for-each select="genotype[chisq/@role!='not-calculated']">  
   <xsl:sort select="@col" data-type="text"/>
   <!-- generate genotype name -->
   <xsl:variable name="name">
    <xsl:value-of select="@col"/>:<xsl:value-of select="@row"/> 
   </xsl:variable>

  <!-- indent table with name of the genotype -->
   <xsl:call-template name="prepend-pad">
    <xsl:with-param name="length" select="$hardyweinberg-first-col-width"/>
    <xsl:with-param name="padVar" select="$name"/>
   </xsl:call-template>
   <!-- generate the row -->
   <xsl:call-template name="hardyweinberg-gen-row"/>
   <xsl:call-template name="newline"/>
  </xsl:for-each>
  <xsl:call-template name="newline"/>
  
  <!-- separator -->
  <xsl:call-template name="separator"/>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- format genotype table for HW -->
 <xsl:template match="genotypetable">

  <xsl:text>Table of genotypes, format of each cell is: observed/expected.</xsl:text>
  <xsl:call-template name="newline"/>

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
     <!-- round and format the decimal values of "observed" to nearest 0.1 -->
     <xsl:value-of select="../observed"/><xsl:text>/</xsl:text><xsl:call-template name="round-to">
      <xsl:with-param name="node" select="../expected"/>
      <xsl:with-param name="places" select="1"/>
     </xsl:call-template>
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

 <!-- print out Guo and Thompson output if it's generated -->
 <xsl:template match="hardyweinbergGuoThompson">
  <xsl:call-template name="locus-header">
   <xsl:with-param name="title">Guo and Thompson HardyWeinberg output</xsl:with-param>
  </xsl:call-template>
  <xsl:choose>
   <xsl:when test="@role='too-few-alleles'">
    <xsl:text>Too few alleles</xsl:text>
   </xsl:when>
   <xsl:when test="@role='too-large-matrix'">
    <xsl:text>Too large a matrix for Guo and Thompson</xsl:text>
   </xsl:when>

   <xsl:otherwise>
    <xsl:choose>
     <!-- only when 1 is produced as a pvalue, we return an error -->
     <xsl:when test="normalize-space(pvalue)='1'">
      <xsl:text>Guo and Thompson test failed to converge.</xsl:text>
     </xsl:when>
     <xsl:otherwise>
      <xsl:call-template name="linesep-fields">
       <xsl:with-param name="nodes" select="pvalue|stderr|dememorizationSteps|samplingNum|samplingSize"/>
      </xsl:call-template>
     </xsl:otherwise>
    </xsl:choose>
    <!--
    <xsl:text>*switches*</xsl:text>
    <xsl:call-template name="newline"/>
    <xsl:call-template name="linesep-fields">
     <xsl:with-param name="nodes" select="switches/*"/>
    </xsl:call-template>
    -->
   </xsl:otherwise>

  </xsl:choose>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <!-- ################  END HARDY-WEINBERG STATISTICS  ############### --> 

 <!-- ################  HOMOZYGOSITY STATISTICS ###################### --> 
 
 <xsl:template match="homozygosity">
  <xsl:call-template name="locus-header">
   <xsl:with-param name="title">Homozygosity</xsl:with-param>
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
    <xsl:apply-templates select="pvalue" mode="bounded"/>
    <xsl:call-template name="newline"/>
   </xsl:otherwise>

  </xsl:choose>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="pvalue">
  <xsl:call-template name="append-pad">
   <xsl:with-param name="padChar">*</xsl:with-param>
   <xsl:with-param name="length">
    <xsl:call-template name="get-significance">
     <xsl:with-param name="pvalue" select="."/>
    </xsl:call-template>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:value-of select="."/> 
 </xsl:template>

 <xsl:template match="pvalue" mode="bounded">
   <xsl:call-template name="append-pad">
   <xsl:with-param name="padChar">*</xsl:with-param>
   <xsl:with-param name="length">
    <xsl:call-template name="get-significance">
     <xsl:with-param name="pvalue" select="upper"/>
    </xsl:call-template>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:text> </xsl:text>
  <xsl:value-of select="lower"/><xsl:text disable-output-escaping="yes"> &lt; pvalue &lt;= </xsl:text><xsl:value-of select="upper"/>
  
  </xsl:template>

 <!-- ################  HOMOZYGOSITY STATISTICS ###################### --> 

 <!-- #################  HAPLOTYPE/LD STATISTICS ###################### --> 

 <xsl:template match="emhaplofreq">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype/LD stats via emhaplofreq: <xsl:value-of select="../@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='no-data']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">No data left after filtering at: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='too-many-lines']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Too many rows for haplotype programme: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='haplo']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype frequency est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>

  <!-- until output is XML-fied, simply pass through the unmarked
  CDATA section -->
  <xsl:apply-templates select="haplotypefreq"/>
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

  <!-- until output sections are XML-fied, simply pass through the
  unmarked CDATA sections -->

  <xsl:value-of select="linkagediseq" disable-output-escaping="yes"/>

  <xsl:value-of select="permutationSummary" disable-output-escaping="yes"/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='haplo-LD']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype frequency and LD est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <!-- until output sections are XML-fied, simply pass through the unmarked
  CDATA sections -->

  <xsl:apply-templates select="haplotypefreq"/>

  <xsl:call-template name="newline"/>

  <xsl:value-of select="linkagediseq" disable-output-escaping="yes"/>
  <xsl:value-of select="permutationSummary" disable-output-escaping="yes"/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="haplotypefreq">

  <!-- loop through each haplotype-->
  <xsl:for-each select="haplotype">
   <xsl:sort select="@name" data-type="text" order="ascending"/>
   <xsl:for-each select="frequency|numCopies|@name">
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="."/>
     <xsl:with-param name="length">24</xsl:with-param>
    </xsl:call-template>
   </xsl:for-each>
   <xsl:call-template name="newline"/>
  </xsl:for-each>

 </xsl:template>


 <!-- ################# END  HAPLOTYPE/LD STATISTICS ################### --> 

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
